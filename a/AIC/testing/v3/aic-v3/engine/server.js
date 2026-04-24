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

app.post('/score', async (req, res) => {
  const { entity } = req.body;

  // TODO: plug in real logic; for now, stubbed example
  const semanticIntelligence = 0.82;
  const culturalMomentum = 0.74;
  const externalCredibility = 0.69;
  const sentimentStability = 0.61;
  const systemConfidence = 0.9;

  const aicNorm =
    0.35 * semanticIntelligence +
    0.25 * culturalMomentum +
    0.20 * externalCredibility +
    0.10 * sentimentStability +
    0.10 * systemConfidence;

  const confidence = systemConfidence; // meta-signal

  res.json({
    entity,
    normalized_score: aicNorm, // 0–1
    components: {
      semantic_intelligence: semanticIntelligence,
      cultural_momentum: culturalMomentum,
      external_credibility: externalCredibility,
      sentiment_stability: sentimentStability,
      system_confidence: systemConfidence
    },
    confidence
  });
});

app.listen(PORT, () => {
    logger.info(`AIC-V3 scoring engine running on port ${PORT}`);
});
