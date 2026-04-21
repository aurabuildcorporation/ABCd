const Sentiment = require("sentiment");
const analyzer = new Sentiment();

module.exports = {
    analyze: (text) => {
        const result = analyzer.analyze(text);
        return (result.score + 5) / 10; // normalize 0–1
    }
};