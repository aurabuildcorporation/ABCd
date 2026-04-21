module.exports = {
    combine: ({ sentiment, embedding, heuristic, volatility, yelp }) => {
        const yelpScore = yelp.rating ? (yelp.rating / 5) : 0;

        const score =
            sentiment * 0.25 +
            embedding * 0.20 +
            heuristic * 0.20 +
            (1 - volatility) * 0.15 +
            yelpScore * 0.20;

        return {
            score: Number(score.toFixed(4)),
            confidence: Number((1 - volatility).toFixed(4)),
            components: {
                sentiment,
                embedding,
                heuristic,
                volatility,
                yelp: yelpScore
            }
        };
    }
};