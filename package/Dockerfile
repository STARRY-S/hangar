FROM suse.hxstarrys.me/bci/golang:1.22 AS builder

WORKDIR /go/src/github.com/cnrancher/hangar/
RUN zypper ref && \
    zypper in -y -f wget vim libbtrfs-devel libgpgme-devel device-mapper-devel git && \
    zypper clean

# pre-copy/cache go.mod for pre-downloading dependencies
# and only redownloading them in subsequent builds if they change
COPY go.mod go.sum ./
RUN go mod download && go mod verify

COPY . .
ENV DISABLE_CGO=''
RUN ./scripts/build.sh

RUN ls -al >> test.txt

FROM suse.hxstarrys.me/bci/bci-base:15.6

WORKDIR /hangar

RUN zypper up -y && \
    zypper in -y -f libdevmapper1_03 bash-completion vim wget && \
    zypper clean && \
    echo "# Add hangar bash completion" >> /root/.bashrc && \
    echo "source <(hangar completion bash)" >> /root/.bashrc

COPY --from=builder /go/src/github.com/cnrancher/hangar/test.txt /
COPY --from=builder /go/src/github.com/cnrancher/hangar/package/entrypoint.sh /
COPY --from=builder /go/src/github.com/cnrancher/hangar/bin/hangar /usr/local/bin/hangar
COPY --from=builder /go/src/github.com/cnrancher/hangar/package/default-policy.json /etc/containers/policy.json
COPY --from=builder /go/src/github.com/cnrancher/hangar/package/registries.d/default.yaml /etc/containers/registries.d/default.yaml

ENTRYPOINT [ "/entrypoint.sh" ]
