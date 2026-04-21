module.exports = {
    vectorScore: (text) => {
        // Placeholder: deterministic pseudo‑embedding score
        let score = 0;
        for (let c of text) score += c.charCodeAt(0);
        return (score % 100) / 100;
    }
};