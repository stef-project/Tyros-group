// Renders the 8 social images (4 variants x FR/EN) from design-system/og/og.html into assets/og/. NODE_PATH=$(npm root -g) node tools/render_og.js
const {chromium}=require('playwright');
const V={default:'og-tyros-group',academy:'og-tyros-academy',search:'og-executive-search',insights:'og-tyros-insights'};
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1200,height:630}});
for(const [v,name] of Object.entries(V))for(const l of ['fr','en']){await p.goto(`http://localhost:8810/design-system/og/og.html?v=${v}&l=${l}`);await p.waitForTimeout(400);
 await p.screenshot({path:`assets/og/${name}-${l}.png`});console.log(name,l)}
await b.close()})()
