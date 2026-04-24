
module.exports = function(entity, base, c){
  const score = (base * 8) + (c.reddit * 40) + (c.wiki * 30) + (c.yelp * 50);

  return {
    entity,
    aic_score: Math.round(score),
    confidence: 0.8,
    components: c
  };
};
