// https://www.shanghairanking.cn/rankings/bcur/202311
console.clear()
const fs = require('fs');
const currentDirectory = __dirname + '/';
jsCode = fetch(`https://www.shanghairanking.cn/_nuxt/static/1680514876/rankings/bcur/2023/payload.js`, {
"method": "GET"
})
.then(response => response.text())
.then(data => {
    jsCode = data;
    jsCode = jsCode.replace(/__NUXT_JSONP__\(".*?",\s/g, 'module.exports = ');
    jsCode = jsCode.replace(/}}\(/g, '}})(');
    jsCode = jsCode.replace(/\)\)\);/g, ');');
    fs.writeFileSync(currentDirectory + 'bcur11.js', jsCode);
    const bcur = require(currentDirectory + 'bcur11.js');
    const jsonData = JSON.parse(JSON.stringify(bcur));
    fs.writeFileSync(currentDirectory + 'bcur11.json', JSON.stringify(jsonData));
    const univData = jsonData['data'][0]['univData'];
    const univList = [];
    for (let i = 0; i < univData.length; i++) {
            const univ = {};
            univ['排名'] = univData[i]['ranking'];
            univ['学校名字'] = univData[i]['univNameCn'];
            univ['省市'] = univData[i]['province'];
            univ['学校类型'] = univData[i]['univCategory'];
            univ['总分'] = univData[i]['score'];
            univ['办学层次'] = univData[i]['indData']["411"]; 
            univ['人才培养'] = univData[i]['indData']["412"]; 
            univ['办学资源'] = univData[i]['indData']["413"]; 
            univ['国际竞争'] = univData[i]['indData']["414"]; 
            univ['学科水平'] = univData[i]['indData']["415"]; 
            univ['师资力量'] = univData[i]['indData']["416"]; 
            univ['服务社会'] = univData[i]['indData']["417"]; 
            univ['科学研究'] = univData[i]['indData']["418"]; 
            univ['重大项目'] = univData[i]['indData']["419"]; 
            univ['高端人才'] = univData[i]['indData']["420"];
            univList.push(univ);
    }
    fs.writeFileSync(currentDirectory + 'result11.json', JSON.stringify(univList));
});