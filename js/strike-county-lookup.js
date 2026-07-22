(() => {
  const select = document.getElementById('county-select');
  const result = document.getElementById('county-result');
  const name = document.getElementById('county-name');
  if (!select || !result || !name) return;

  const counties = ['Baker','Benton','Clackamas','Clatsop','Columbia','Coos','Crook','Curry','Deschutes','Douglas','Gilliam','Grant','Harney','Hood River','Jackson','Jefferson','Josephine','Klamath','Lake','Lane','Lincoln','Linn','Malheur','Marion','Morrow','Multnomah','Polk','Sherman','Tillamook','Umatilla','Union','Wallowa','Wasco','Washington','Wheeler','Yamhill'];
  counties.forEach((county) => {
    const option = document.createElement('option');
    option.value = county;
    option.textContent = `${county} County`;
    select.append(option);
  });

  const update = () => {
    if (!select.value) {
      result.hidden = true;
      return;
    }
    name.textContent = `${select.value} County`;
    result.hidden = false;
  };
  select.addEventListener('change', update);
  update();
})();
