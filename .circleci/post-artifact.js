#!/usr/bin/env node
 
const bot = require("circle-github-bot").create();

var fs = require("fs");
var files = fs.readdirSync("/tmp");
console.log(files);

bot.comment(process.env.GH_AUTH_TOKEN, `
<h3>${bot.env.commitMessage}</h3>
${files}
`);