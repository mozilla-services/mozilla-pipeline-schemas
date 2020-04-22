#!/usr/bin/env node
// A script for posting to Github from CircleCI. This requires GH_AUTH_TOKEN to
// be set up, along-side CircleCI specific variables. See the source at [1] for
// more details.
// https://github.com/themadcreator/circle-github-bot/blob/master/src/index.ts

const fs = require("fs");
const bot = require("circle-github-bot").create();

let root = "/tmp/test-reports";
let files = fs.readdirSync(root);
console.log(files);
console.log(fs.readdirSync("/tmp/integration"));

// An example listing of files. The diff is created by comparing differences
// between the upstream commit (mozilla-pipeline-schemas/master) and the report
// generated from the PR
//
// ["723350e.report.json", "c88ebe5.report.json", "c88ebe5-723350e.diff"]

let diff_file = files.filter(x => x.endsWith(".diff"))[0];
let diff_content = fs.readFileSync(root + "/" + diff_file, "utf8");
let [upstream, head] = diff_file.split(".")[0].split("-");

// Generate and post markdown
var content = `#### \`${diff_file}\`
\`\`\`diff
${diff_content}
\`\`\`
`;

if (!diff_content) {
    content =  "No changes detected.";
}

bot.comment(process.env.GH_AUTH_TOKEN, `
### Integration report for "${bot.env.commitMessage}"
[Report for upstream](${bot.env.buildUrl}/artifacts/0/app/test-reports/${upstream}.report.json)
[Report for latest commit](${bot.env.buildUrl}/artifacts/0/app/test-reports/${head}.report.json)

${content}
`);
