import cloud from "../../public/data/cloud.json";
import ai from "../../public/data/ai.json";
import devops from "../../public/data/devops.json";
import finops from "../../public/data/finops.json";
import secops from "../../public/data/secops.json";

const map = {
  cloud,
  ai,
  devops,
  finops,
  secops
};

export function getNews(category) {
  return map[category] || [];
}
