(() => {
  const select = document.getElementById('county-select');
  const result = document.getElementById('county-result');
  const countyName = document.getElementById('county-name');
  const agencyName = document.getElementById('county-agency-name');
  const agencyPhone = document.getElementById('county-agency-phone');
  const agencyLink = document.getElementById('county-agency-link');
  if (!select || !result || !countyName || !agencyName || !agencyPhone || !agencyLink) return;

  const agencies = {
    access: { name: 'ACCESS, Inc.', phone: '541-779-6691', phoneHref: 'tel:+15417796691', url: 'https://accesshelps.org/' },
    caowash: { name: 'Community Action Organization', phone: '503-648-6646', phoneHref: 'tel:+15036486646', url: 'https://caowash.org/' },
    capeco: { name: 'Community Action Program of East Central Oregon (CAPECO)', phone: '800-752-1139', phoneHref: 'tel:+18007521139', url: 'https://www.capeco-works.org/' },
    cat: { name: 'Community Action Team', phone: '503-397-3511', phoneHref: 'tel:+15033973511', url: 'https://cat-team.org/' },
    ccno: { name: 'Community Connection of Northeast Oregon', phone: '541-963-3186', phoneHref: 'tel:+15419633186', url: 'https://ccno.org/' },
    clackamas: { name: 'Clackamas County Social Services', phone: '503-655-8640', phoneHref: 'tel:+15036558640', url: 'https://www.clackamas.us/socialservices' },
    communityInAction: { name: 'Community in Action', phone: '541-889-1060 ext. 101', phoneHref: 'tel:+15418891060', url: 'https://communityinaction.info/' },
    csc: { name: 'Community Services Consortium', phone: '541-928-6335', phoneHref: 'tel:+15419286335', url: 'https://communityservices.us/' },
    klcas: { name: 'Klamath & Lake Community Action Services', phone: '541-882-3500', phoneHref: 'tel:+15418823500', url: 'https://www.klcas.org/' },
    lane: { name: 'Lane County Human Services Division', phone: '541-682-3378', phoneHref: 'tel:+15416823378', url: 'https://www.lanecounty.org/government/county_departments/health_and_human_services/human_services_division' },
    mccac: { name: 'Mid-Columbia Community Action Council', phone: '541-298-5131', phoneHref: 'tel:+15412985131', url: 'https://www.mccac.com/' },
    multnomah: { name: 'Multnomah County Human Services Division', phone: '503-988-3691', phoneHref: 'tel:+15039883691', url: 'https://www.multco.us/dchs' },
    mwvcaa: { name: 'Mid-Willamette Valley Community Action Agency', phone: '503-399-9080', phoneHref: 'tel:+15033999080', url: 'https://mwvcaa.org/' },
    neighborImpact: { name: 'NeighborImpact', phone: '541-548-2390', phoneHref: 'tel:+15415482390', url: 'https://www.neighborimpact.org/' },
    orcca: { name: 'Oregon Coast Community Action', phone: '541-435-7746', phoneHref: 'tel:+15414357746', url: 'https://www.orcca.us/' },
    ucan: { name: 'United Community Action Network', phone: '800-301-8226', phoneHref: 'tel:+18003018226', url: 'https://www.ucancap.org/' },
    ycap: { name: 'Yamhill Community Action Partnership', phone: '503-472-0457', phoneHref: 'tel:+15034720457', url: 'https://yamhillcap.org/' },
  };

  const countyAgencies = {
    Baker: 'ccno',
    Benton: 'csc',
    Clackamas: 'clackamas',
    Clatsop: 'cat',
    Columbia: 'cat',
    Coos: 'orcca',
    Crook: 'neighborImpact',
    Curry: 'orcca',
    Deschutes: 'neighborImpact',
    Douglas: 'ucan',
    Gilliam: 'capeco',
    Grant: 'ccno',
    Harney: 'communityInAction',
    'Hood River': 'mccac',
    Jackson: 'access',
    Jefferson: 'neighborImpact',
    Josephine: 'ucan',
    Klamath: 'klcas',
    Lake: 'klcas',
    Lane: 'lane',
    Lincoln: 'csc',
    Linn: 'csc',
    Malheur: 'communityInAction',
    Marion: 'mwvcaa',
    Morrow: 'capeco',
    Multnomah: 'multnomah',
    Polk: 'mwvcaa',
    Sherman: 'mccac',
    Tillamook: 'cat',
    Umatilla: 'capeco',
    Union: 'ccno',
    Wallowa: 'ccno',
    Wasco: 'mccac',
    Washington: 'caowash',
    Wheeler: 'capeco',
    Yamhill: 'ycap',
  };

  const counties = Object.keys(countyAgencies);
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

    const agency = agencies[countyAgencies[select.value]];
    countyName.textContent = `${select.value} County`;
    agencyName.textContent = agency.name;
    agencyPhone.textContent = agency.phone;
    agencyPhone.href = agency.phoneHref;
    agencyPhone.setAttribute('aria-label', `Call ${agency.name} at ${agency.phone}`);
    agencyLink.href = agency.url;
    agencyLink.setAttribute('aria-label', `Visit ${agency.name} website`);
    result.hidden = false;
  };

  select.addEventListener('change', update);
  update();
})();
