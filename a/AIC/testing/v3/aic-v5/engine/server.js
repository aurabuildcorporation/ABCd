const express = require("express");
const bodyParser = require("body-parser");
const sentiment = require("./scoring/sentiment");
const embeddings = require("./scoring/embeddings");
const heuristics = require("./scoring/heuristics");
const volatility = require("./scoring/volatility");
const fusion = require("./scoring/fusion");
const yelp = require("./scoring/yelp_enrichment");
const logger = require("./utils/logger");

require("dotenv").config();

const app = express();
app.use(bodyParser.json());

const PORT = process.env.NODE_ENGINE_PORT || 7000;

app.post("/score", async (req, res) => {
    const entity = req.body.entity;

    if (!entity) {
        return res.status(400).json({ error: "Missing entity" });
    }

    logger.info(`Scoring entity: ${entity}`);

    try {
        const sentimentScore = sentiment.analyze(entity);
        const embeddingScore = embeddings.vectorScore(entity);
        const heuristicScore = heuristics.apply(entity);
        const volatilityScore = volatility.measure(entity);
        const yelpData = await yelp.enrich(entity);

        const finalScore = fusion.combine({
            sentiment: sentimentScore,
            embedding: embeddingScore,
            heuristic: heuristicScore,
            volatility: volatilityScore,
            yelp: yelpData
        });

        return res.json(finalScore);

    } catch (err) {
        logger.error(err.toString());
        return res.status(500).json({ error: err.toString() });
    }
});

app.listen(PORT, () => {
    logger.info(`AIC-V3 scoring engine running on port ${PORT}`);
});