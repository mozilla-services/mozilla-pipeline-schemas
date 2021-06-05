#!/usr/bin/env node
// A script for posting to Github from CircleCI. This requires GH_AUTH_TOKEN to
// be set up, along-side CircleCI specific variables. See the source at [1] for
// more details.
// https://github.com/themadcreator/circle-github-bot/blob/master/src/index.ts

const fs = require("fs");
const bot = require("circle-github-bot").create();


function diff(prefix) {
    let root = "/tmp/integration";
    let files = fs.readdirSync(root);
    console.log(files);
    let diff_file = files.find(x => x.startsWith(prefix) && x.endsWith(".diff"));
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

${diff("bq_schema")}

${diff("compact_schema")}
`);
