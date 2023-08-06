import torch
import torch.nn as nn
from torch.nn.utils.weight_norm import weight_norm
from multimodal.text import WordEmbedding
import pytorch_lightning as pl


class QuestionEmbedding(nn.Module):
    def __init__(self, in_dim, num_hid, nlayers, bidirect, dropout):
        """Module for question embedding
        """
        super(QuestionEmbedding, self).__init__()
        self.rnn = nn.GRU(
            in_dim,
            num_hid,
            nlayers,
            bidirectional=bidirect,
            dropout=dropout,
            batch_first=True,
        )

        self.in_dim = in_dim
        self.num_hid = num_hid
        self.nlayers = nlayers
        self.ndirections = 1 + int(bidirect)

    def init_hidden(self, batch):
        # just to get the type of tensor
        weight = next(self.parameters()).data
        hid_shape = (self.nlayers * self.ndirections, batch, self.num_hid)
        return weight.new(*hid_shape).zero_()

    def forward(self, x):
        # x: [batch, sequence, in_dim]
        batch = x.size(0)
        hidden = self.init_hidden(batch)
        self.rnn.flatten_parameters()
        output, hidden = self.rnn(x, hidden)

        if self.ndirections == 1:
            return output[:, -1]

        forward_ = output[:, -1, : self.num_hid]
        backward = output[:, 0, self.num_hid :]
        return torch.cat((forward_, backward), dim=1)

    def forward_all(self, x):
        # x: [batch, sequence, in_dim]
        batch = x.size(0)
        hidden = self.init_hidden(batch)
        self.rnn.flatten_parameters()
        output, hidden = self.rnn(x, hidden)
        return output


class SimpleClassifier(nn.Module):
    def __init__(self, in_dim, hid_dim, out_dim, dropout):
        super(SimpleClassifier, self).__init__()
        layers = [
            weight_norm(nn.Linear(in_dim, hid_dim), dim=None),
            nn.ReLU(),
            nn.Dropout(dropout, inplace=True),
            weight_norm(nn.Linear(hid_dim, out_dim), dim=None),
        ]
        self.main = nn.Sequential(*layers)

    def forward(self, x):
        logits = self.main(x)
        return logits


class FCNet(nn.Module):
    """Simple class for non-linear fully connect network
    """

    def __init__(self, dims):
        super(FCNet, self).__init__()

        layers = []
        for i in range(len(dims) - 2):
            in_dim = dims[i]
            out_dim = dims[i + 1]
            layers.append(weight_norm(nn.Linear(in_dim, out_dim), dim=None))
            layers.append(nn.ReLU())
        layers.append(weight_norm(nn.Linear(dims[-2], dims[-1]), dim=None))
        layers.append(nn.ReLU())

        self.main = nn.Sequential(*layers)

    def forward(self, x):
        return self.main(x)


class Attention(nn.Module):
    def __init__(self, v_dim, q_dim, num_hid):
        super(Attention, self).__init__()
        self.nonlinear = FCNet([v_dim + q_dim, num_hid])
        self.linear = weight_norm(nn.Linear(num_hid, 1), dim=None)

    def forward(self, v, q):
        """
        v: [batch, k, vdim]
        q: [batch, qdim]
        """
        logits = self.logits(v, q)
        w = nn.functional.softmax(logits, 1)
        return w

    def logits(self, v, q):
        num_objs = v.size(1)
        q = q.unsqueeze(1).repeat(1, num_objs, 1)
        vq = torch.cat((v, q), 2)
        joint_repr = self.nonlinear(vq)
        logits = self.linear(joint_repr)
        return logits


class UpDownModel(nn.Module):
    def __init__(
        self, num_ans, v_dim, num_hid, tokens=None, dir_data=None,
    ):
        super().__init__()
        self.w_emb = WordEmbedding.from_pretrained(
            "glove.6B.300d", tokens=tokens, dir_data=dir_data
        )
        self.q_emb = QuestionEmbedding(300, num_hid, 1, False, 0.0)
        self.v_att = Attention(v_dim, self.q_emb.num_hid, num_hid)
        self.q_net = FCNet([self.q_emb.num_hid, num_hid])
        self.v_net = FCNet([v_dim, num_hid])
        self.classifier = SimpleClassifier(num_hid, num_hid * 2, num_ans, 0.5)

    def forward(self, batch):
        """Forward
        v: [batch, num_objs, obj_dim]
        b: [batch, num_objs, b_dim]
        q: [batch_size, seq_length]
        return: logits, not probs
        """
        # breakpoint()
        v = batch["features"]
        q = batch["question"]

        w_emb = self.w_emb(q)
        q_emb = self.q_emb(w_emb)  # [batch, q_dim]

        att = self.v_att(v, q_emb)

        v_emb = (att * v).sum(1)  # [batch, v_dim]
        q_repr = self.q_net(q_emb)
        v_repr = self.v_net(v_emb)
        joint_repr = q_repr * v_repr
        logits = self.classifier(joint_repr)
        out = {
            "logits": logits,
            "mm": joint_repr,
            "processed_question": q_emb,
        }
        return out

    @classmethod
    def from_pretrained(cls, name="updown-base"):
        """
        One of "updown-base-100, updown-base-36, updown-newatt-100, updown-newatt-36
        """
        pass


class VQALightningModule(pl.LightningModule):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.loss = nn.BCEWithLogitsLoss()

    def training_step(self, batch, batch_idx):
        out = self.model(batch)
        logits = out["logits"]
        loss = self.loss(logits, batch["label"])
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        out = self.model(batch)
        logits = out["logits"]
        loss = self.loss(logits, batch["label"])
        self.log("val_loss", loss)
        return loss

    def test_step(self, batch, batch_idx):
        out = self.model(batch)
        logits = out["logits"]
        loss = self.loss(logits, batch["label"])
        self.log("val_loss", loss)
        return loss

    def forward(self, batch):
        return self.model(batch)

    def configure_optimizers(self):
        optim = torch.optim.Adamax(self.parameters())
        return optim

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--dir-data", required=True)
    parser.add_argument("--v_dim", type=int, default=2048)
    parser.add_argument("--num_hid", type=int, default=2048)
    parser.add_argument("--batch-size", default=512, type=int)
    parser.add_argument("--min-ans-occ", default=9, type=int)
    parser.add_argument("--features", default="coco-bottomup-36")
    args = parser.parse_args()

    from multimodal.datasets import VQA2DataModule

    vqa2 = VQA2DataModule(
        dir_data=args.dir_data,
        min_ans_occ=args.min_ans_occ,
        features=args.features,
        label="multilabel",
        batch_size=args.batch_size,
    )

    trainloader = vqa2.train_dataloader()
    tokens = trainloader.dataset.get_all_tokens()
    num_ans = len(trainloader.dataset.answers)
    updown = UpDownModel(
        num_ans=num_ans,
        v_dim=args.v_dim,
        num_hid=args.num_hid,
        tokens=tokens,
        dir_data=args.dir_data,
    )

    lightningmodel = VQALightningModule(updown)

    trainer = pl.Trainer(gpus=1, max_epochs=30)
    trainer.fit(lightningmodel, datamodule=vqa2)
