const axios = require("axios");

module.exports = {
    enrich: async (term) => {
        const apiKey = process.env.YELP_API_KEY;
        if (!apiKey) return { rating: 0, reviews: 0 };

        try {
            const res = await axios.get(
                "https://api.yelp.com/v3/businesses/search",
                {
                    headers: { Authorization: `Bearer ${apiKey}` },
                    params: { term, location: "San Francisco", limit: 1 }
                }
            );

            const biz = res.data.businesses?.[0];
            if (!biz) return { rating: 0, reviews: 0 };

            return {
                rating: biz.rating || 0,
                reviews: biz.review_count || 0
            };

        } catch (err) {
            return { rating: 0, reviews: 0 };
        }
    }
};