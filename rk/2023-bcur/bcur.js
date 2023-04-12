// https://www.shanghairanking.cn/rankings/bcur/2023
// npm install 安装依赖
console.clear()
const fs = require('fs');

// 分榜下载
function saveResult(id, nameCn) {
    jsCode = fetch(`https://www.shanghairanking.cn/_nuxt/static/1680514876/rankings/bcur/2023${id}/payload.js`, {
        "method": "GET"
    })
    .then(response => response.text())
    .then(data => {
        jsCode = data;
        jsCode = jsCode.replace(/__NUXT_JSONP__\(".*?",\s/g, 'module.exports = ');
        jsCode = jsCode.replace(/}}\(/g, '}})(');
        jsCode = jsCode.replace(/\)\)\);/g, ');');
        fs.writeFileSync(`${__dirname}/${nameCn}.js`, jsCode);
        const bcur = require(`${__dirname}/${nameCn}.js`);
        fs.unlinkSync(`${__dirname}/${nameCn}.js`)
        const jsonData = JSON.parse(JSON.stringify(bcur));
        // 分析 json 格式
        // fs.writeFileSync(currentDirectory + `${nameCn}.json`, JSON.stringify(jsonData));
        // process.abort()
        const univData = jsonData['data'][0]['univData'];
        const univList = [];
        for (let i = 0; i < univData.length; i++) {
            const univ = {};
            // 主榜
            if (id == 11){
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
            }
            // 艺术
            else if (id == 30){
                univ['学校名字'] = univData[i]['univNameCn'];
                univ['省市'] = univData[i]['province'];
                univ['硕士点'] = univData[i]['531'];
                univ['博士点'] = univData[i]['532'];
                univ['国家一流本科专业'] = univData[i]['533'];
                univ['本科毕业生就业率'] = univData[i]['534']; 
                univ['本科毕业生深造率'] = univData[i]['535']; 
            }
            else if (id == 10 || id == 15 || id == -15) {
                univ['排名'] = univData[i]['ranking'];
                univ['学校名字'] = univData[i]['univNameCn'];
                univ['省市'] = univData[i]['province'];
                univ['学校类型'] = univData[i]['univCategory'];
                univ['总分'] = univData[i]['score'];
            }
            else {
                univ['排名'] = univData[i]['ranking'];
                univ['学校名字'] = univData[i]['univNameCn'];
                univ['省市'] = univData[i]['province'];
                univ['学校类型'] = univData[i]['univCategory'];
                univ['总分'] = univData[i]['score'];
                univ['全国参考排名'] = univData[i]['rankOverall']; 
            }
            univList.push(univ);
        }
        // fs.writeFileSync(`${__dirname}/${nameCn}.json`, JSON.stringify(univList));
        const XLSX = require('xlsx');
        const worksheet = XLSX.utils.json_to_sheet(JSON.parse(JSON.stringify(univList)));
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');
        XLSX.writeFile(workbook, `${__dirname}/${nameCn}.xlsx`);
    });
}

jsCode = fetch(`https://www.shanghairanking.cn/_nuxt/static/1680514876/rankings/bcur/2023/payload.js`, {
"method": "GET"
})
.then(response => response.text())
.then(data => {
    jsCode = data;
    jsCode = jsCode.replace(/__NUXT_JSONP__\(".*?",\s/g, 'module.exports = ');
    jsCode = jsCode.replace(/}}\(/g, '}})(');
    jsCode = jsCode.replace(/\)\)\);/g, ');');
    fs.writeFileSync(`${__dirname}/bcur11.js`, jsCode);
    const bcur = require(`${__dirname}/bcur11.js`);
    fs.unlinkSync(`${__dirname}/bcur11.js`)
    const jsonData = JSON.parse(JSON.stringify(bcur));
    var rankList = jsonData['data'][0]['bcurTypes'];
    for (var i = 0; i < rankList.length; i++) {
        const rankingID = rankList[i]['id']
        const nameCn = rankList[i]['nameCn']
        if (fs.existsSync(`${__dirname}/${nameCn}.xlsx`) == false && rankingID != 12 && rankingID != 13)
            saveResult(rankingID, nameCn)
        console.log(`=> ${nameCn}`)
    }
});