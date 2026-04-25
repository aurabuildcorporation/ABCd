const express = require("express");
const axios = require("axios");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

app.post("/score", async (req, res) => {
    try {
        const entity = req.body.entity;

        const response = await axios.post(
            "http://localhost:5000/score",
            { entity }
        );

        res.json(response.data);

    } catch (err) {
        res.status(500).json({
            error: "Scoring engine offline"
        });
    }
});

// fetch entity history from python
app.get("/history/:entity", async (req, res) => {
    try {
        const entity = req.params.entity;

        const response = await axios.get(
            `http://localhost:5000/history/${entity}`
        );

        res.json(response.data);

    } catch (err) {
        res.status(500).json({ error: "History unavailable" });
    }
});

app.listen(3000, () => {
    console.log("AIC Backend running :3000");
});
