package manifest

import (
	"context"
	"fmt"
	"net/url"
	"testing"

	"github.com/containers/image/v5/image"
	"github.com/containers/image/v5/types"
)

func Test_parseImageSource(t *testing.T) {
	u, err := url.Parse("docker://h2.hxstarrys.me:30003/library/nginx:1.22")
	if err != nil {
		t.Error(err)
		return
	}
	fmt.Printf("host: %v\n", u.Host)

	src, err := parseImageSource(context.TODO(),
		"docker://h2.hxstarrys.me:30003/library/nginx:1.22")
	if err != nil {
		t.Error(err)
		return
	}
	raw, mime, err := src.GetManifest(context.TODO(), nil)
	if err != nil {
		t.Error(err)
		return
	}
	fmt.Printf("raw: %v\n", string(raw)) // RAW manifest
	fmt.Printf("str: %v\n", mime)        // MIME Type

	img, err := image.FromUnparsedImage(
		context.TODO(),
		&types.SystemContext{
			OSChoice:           "linux",
			ArchitectureChoice: "amd64",
		},
		image.UnparsedInstance(src, nil))
	if err != nil {
		t.Errorf("Error parsing manifest for image: %v", err)
		return
	}
	config, err := img.ConfigBlob(context.TODO())
	if err != nil {
		t.Error(err)
		return
	}
	fmt.Printf("config: %v\n", string(config)) // MIME Type
}
