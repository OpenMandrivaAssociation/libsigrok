name=$(cat *.spec | grep -i Name: | awk '{print $NF}')
date=$(date +%Y%m%d)
#repo_url=$(cat *.spec | grep -i URL: | awk '{print $NF}')
git clone --depth 1 https://github.com/sigrokproject/libsigrok $name
cd $name
gitcommit=$(git rev-parse --short HEAD)
git archive --format=tar --prefix $name-$(date +%Y%m%d)-$gitcommit/ HEAD | zstd --ultra -22 > ../$name-$date-$gitcommit.tar.zst
sed -i -E "s:%define sourcedate [0-9]+:%define sourcedate $date:g" ../$name.spec
sed -i -E "s:%define gitcommit [a-z0-9]+:%define gitcommit $gitcommit:g" ../$name.spec
echo "sourcedate define value: ${date}"
echo "gitcommit deifne value: ${gitcommit}"
cd -
