if (process.argv.includes("--help") || process.argv.includes("-h")) {
  console.log(`usage: node extract-tags.js < spec.yml

Reads a Clerk OpenAPI YAML document from stdin and writes one tag name per line
to stdout. Diagnostics and invalid-input errors are written to stderr.`);
  process.exit(0);
}

let input = "";
process.stdin.on("data", d => input += d);
process.stdin.on("end", () => {
  const lines = input.replace(/\r/g, "").split("\n");
  let inTags = false;
  for (const line of lines) {
    if (line === "tags:") { inTags = true; continue; }
    if (inTags && line.length > 0 && line[0] !== " ") break;
    if (inTags) {
      const m = line.match(/^\s{2}- name:\s*(.+)/);
      if (m) console.log(m[1]);
    }
  }
});
