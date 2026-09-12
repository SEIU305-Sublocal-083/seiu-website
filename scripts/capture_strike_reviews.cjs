// Capture rendered previews and check the chosen citation display with keyboard input.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '..');
const folder = path.join(root, 'test-pages/strike-2026');
const requested = process.argv[2];
const origin = process.env.LOCAL083_REVIEW_ORIGIN || 'http://127.0.0.1:8765';
const digest = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const entries = fs.readdirSync(folder).filter(id => fs.existsSync(path.join(folder, id, 'item.json')) && (!requested || id === requested));
  const targets = [];
  if (!requested || requested === 'REVIEW') targets.push({id:'REVIEW',dir:folder,citations:'none',variants:[{key:'overview',file:'index.html'}]});
  for (const id of entries) {
    const dir = path.join(folder,id);
    const item = JSON.parse(fs.readFileSync(path.join(dir,'item.json'),'utf8'));
    targets.push({id,dir,citations:item.citations,variants:item.variants.flatMap(v => ['en','es'].filter(lang => fs.existsSync(path.join(dir,`${v.key}.${lang}.html`))).map(lang => ({key:`${v.key}-${lang}`,file:`${v.key}.${lang}.html`})))});
  }
  const failures = [];
  for (const target of targets) {
    const report = {item:target.id,capture_method:'Playwright screenshot of local rendered HTML',citation_display:target.citations,pages:[]};
    fs.mkdirSync(path.join(target.dir,'screenshots'),{recursive:true});
    for (const variant of target.variants) {
      const localPath = path.relative(root,path.join(target.dir,variant.file)).split(path.sep).join('/');
      for (const [name,width,height] of [['desktop',1440,1000],['mobile',390,844]]) {
        const context = await browser.newContext({viewport:{width,height},deviceScaleFactor:1,reducedMotion:'reduce'});
        // Previews are local and contain no analytics. Catch unintended external fetches.
        await context.route('**/*', route => route.request().url().startsWith(origin+'/') ? route.continue() : route.abort());
        const page = await context.newPage();
        const errors=[];
        page.on('pageerror', e=>errors.push(e.message));
        page.on('response', r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`)});
        await page.goto(`${origin}/${localPath}`,{waitUntil:'networkidle'});
        await page.evaluate(()=>document.fonts.ready);
        const qa=await page.evaluate(()=>({
          title:document.title,
          h1:document.querySelectorAll('h1').length,
          horizontalOverflow:document.documentElement.scrollWidth>innerWidth+1,
          brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.getAttribute('src')),
          citationSections:document.querySelectorAll('.sources').length,
          citationsClosedInitially:!document.querySelector('.sources') || (document.querySelector('.sources').tagName==='DETAILS' && !document.querySelector('.sources').open),
          noindex:document.querySelector('meta[name="robots"]')?.content,
          height:document.documentElement.scrollHeight,
          links:[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'))
        }));
        const citationPolicyMatches=qa.citationSections===(target.citations==='collapsed'?1:0) && qa.citationsClosedInitially;
        if(qa.h1!==1||qa.horizontalOverflow||qa.brokenImages.length||!citationPolicyMatches||qa.noindex!=='noindex,nofollow'||errors.length)failures.push({item:target.id,variant:variant.key,viewport:name,qa,errors});
        const filename=`${variant.key}-${name}-full.png`;
        await page.screenshot({path:path.join(target.dir,'screenshots',filename),fullPage:true});
        if(variant===target.variants[0])await page.screenshot({path:path.join(target.dir,'screenshots',`${name}.png`)});
        let expandedSources;
        if(target.citations==='collapsed'){
          const summary=page.locator('details.sources > summary');
          await summary.focus();
          await page.keyboard.press('Enter');
          const expanded=await page.evaluate(()=>({open:document.querySelector('details.sources').open,contentVisible:document.querySelector('.sources-body').getBoundingClientRect().height>0,referenceLinks:document.querySelectorAll('.sources-body a[href]').length,horizontalOverflow:document.documentElement.scrollWidth>innerWidth+1}));
          const expandedFilename=`${variant.key}-${name}-sources-expanded-full.png`;
          await page.screenshot({path:path.join(target.dir,'screenshots',expandedFilename),fullPage:true});
          await summary.focus();
          await page.keyboard.press('Space');
          const closedAgain=await page.locator('details.sources').evaluate(node=>!node.open);
          qa.citationKeyboardToggle=expanded.open&&expanded.contentVisible&&expanded.referenceLinks>0&&!expanded.horizontalOverflow&&closedAgain;
          if(!qa.citationKeyboardToggle)failures.push({item:target.id,variant:variant.key,viewport:name,expanded,closedAgain});
          expandedSources={screenshot:`screenshots/${expandedFilename}`,screenshot_sha256:digest(path.join(target.dir,'screenshots',expandedFilename)),qa:expanded};
        }
        report.pages.push({file:variant.file,html_sha256:digest(path.join(target.dir,variant.file)),viewport:{name,width,height},screenshot:`screenshots/${filename}`,screenshot_sha256:digest(path.join(target.dir,'screenshots',filename)),expanded_sources:expandedSources,qa:{...qa,links:undefined},errors});
        await context.close();
      }
    }
    fs.writeFileSync(path.join(target.dir,'screenshots','capture-report.json'),JSON.stringify(report,null,2)+'\n');
    console.log(`${target.id}: ${report.pages.length} full-page captures`);
  }
  await browser.close();
  if(failures.length){console.error(JSON.stringify(failures,null,2));process.exit(1)}
  console.log('PASS: citation display and keyboard toggles match policy; previews have one heading, loaded images and no page-level horizontal overflow.');
})().catch(e=>{console.error(e);process.exit(1)});
