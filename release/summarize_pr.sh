#
# Summarize pull requests.  Example usage:
#
#   bash summarize_pr.sh 123 456 789
#
# where 123, 456 and 789 are PR IDs.  List as many PRs as you want.
#
# You can paste this directly into CHANGELOG.md
#
for prid in "$@"
do
    api_url="https://api.github.com/repos/RaRe-Technologies/sqlitedict/pulls/${prid})"
    json="$(wget --quiet -O - ${api_url})"
    title="$(echo "$json" | jq .title --raw-output)"
    html_url="$(echo "$json" | jq .html_url --raw-output)"
    user="$(echo "$json" | jq .user.login --raw-output)"
    user_html_url="$(echo "$json" | jq .user.html_url --raw-output)"
    echo "* ${title} (PR [#${prid}](${html_url}), [@${user}](${user_html_url}))"
done
