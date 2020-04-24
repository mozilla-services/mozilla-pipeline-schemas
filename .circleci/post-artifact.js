#!/usr/bin/env node
// A script for posting to Github from CircleCI. This requires GH_AUTH_TOKEN to
// be set up, along-side CircleCI specific variables. See the source at [1] for
// more details.
// https://github.com/themadcreator/circle-github-bot/blob/master/src/index.ts

const fs = require("fs");
const bot = require("circle-github-bot").create();

function validation_report() {
    let root = "/tmp/test-reports";
    let files = fs.readdirSync(root);
    console.log(files);

    // An example listing of files. The diff is created by comparing differences
    // between the upstream commit (mozilla-pipeline-schemas/master) and the report
    // generated from the PR
    //
    // ["723350e.report.json", "c88ebe5.report.json", "c88ebe5-723350e.diff"]

    let diff_file = files.find(x => x.endsWith(".diff"));
    let diff_content = fs.readFileSync(root + "/" + diff_file, "utf8");
    let [upstream, head] = diff_file.split(".")[0].split("-");

    var body = "No content detected.";
    if (diff_content) {
        body = `<details>
<summary>Click to expand!</summary>

\`\`\`diff
${diff_content}
\`\`\`
</details>
`;
    }

    // Generate and post markdown
    let content = `
[Report for upstream](${bot.env.buildUrl}/artifacts/0/app/test-reports/${upstream}.report.json)
[Report for latest commit](${bot.env.buildUrl}/artifacts/0/app/test-reports/${head}.report.json)

#### \`${diff_file}\`
${body}
`;
    return content;
}

function bigquery_diff() {
    let root = "/tmp/integration";
    let files = fs.readdirSync(root);
    console.log(files);
    let diff_file = files.find(x => x.endsWith(".diff"));
    let diff_content = fs.readFileSync(root + "/" + diff_file, "utf8");

    var body = "No content detected."
    if (diff_content) {
        body = `<details>
<summary>Click to expand!</summary>

\`\`\`diff
${diff_content}
\`\`\`
</details>
`
    }
    var content = `#### \`${diff_file}\`
${body}
`;
    return content;
}

bot.comment(process.env.GH_AUTH_TOKEN, `
### Integration report for "${bot.env.commitMessage}"
${validation_report()}

${bigquery_diff()}
`);
