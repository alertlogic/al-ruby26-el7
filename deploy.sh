set -ex

# if local build, exit
if [ -z "${CODEBUILD_BUILD_IMAGE}" ]; then
  exit 0
fi

# download latest external dependancies
mkdir -p RPMS/{x86_64,noarch}/
yumdownloader --destdir=RPMS/x86_64/ \
  rh-ruby26-rubygem-psych \
  rh-ruby26-ruby-libs \
  rh-ruby26-rubygem-did_you_mean \
  rh-ruby26-rubygem-io-console \
  rh-ruby26-ruby \
  rh-ruby26-ruby-devel \
  rh-ruby26-runtime \
  rh-ruby26-rubygem-json \
  rh-ruby26-rubygem-bigdecimal \
  rh-ruby26-rubygem-openssl

yumdownloader --destdir=RPMS/noarch/ \
  rh-ruby26-ruby-irb \
  rh-ruby26-rubygem-rdoc \
  rh-ruby26-rubygems \
  rh-ruby26-rubygems-devel

# upload files
DISTRIBUTION="el7"
RELEASE_DIRS="dev"
# if production release, add prod
if [ ! -z "${PROD_RELEASE}" ]; then
  RELEASE_DIRS="${RELEASE_DIRS} prod"
fi
for RELEASE_DIR in $RELEASE_DIRS; do
  for DIR in RPMS SRPMS SPECS SOURCES; do
    aws s3 cp --recursive ./${DIR}/ s3://${S3REPOBUCKET}/${RELEASE_DIR}/${DISTRIBUTION}/${DIR}/
  done
done
