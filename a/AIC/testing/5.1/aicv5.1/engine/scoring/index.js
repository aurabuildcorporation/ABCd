
const fuse = require("./fusion");

module.exports = async function(entity, type, mode){
  const base = Math.random() * 100;

  const components = {
    reddit: Math.random(),
    wiki: Math.random(),
    yelp: type === "business" ? Math.random() : 0.2
  };

  return fuse(entity, base, components);
};
