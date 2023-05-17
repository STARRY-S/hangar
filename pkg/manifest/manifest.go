package manifest

import (
	"context"
	"fmt"

	"github.com/containers/image/v5/image"
	"github.com/containers/image/v5/transports/alltransports"
	"github.com/containers/image/v5/types"
)

// parseImageSource converts image URL-like string to an ImageSource.
// The caller must call .Close() on the returned ImageSource.
func parseImageSource(ctx context.Context, name string) (types.ImageSource, error) {
	ref, err := alltransports.ParseImageName(name)
	if err != nil {
		return nil, err
	}
	sysCtx := &types.SystemContext{
		DockerAuthConfig: &types.DockerAuthConfig{},
	}
	if err != nil {
		return nil, err
	}
	return ref.NewImageSource(ctx, sysCtx)
}

type Inspecter struct {
	Ctx context.Context

	Name             string // image name (URL format docker://image:tag)
	DockerAuthConfig *types.DockerAuthConfig

	Raw    bool
	Config bool

	SkipTlsVerify bool

	OverrideOs      string
	OverrideArch    string
	OverrideVariant string
}

func (ins *Inspecter) Inspect() (manifest, mime string, err error) {
	ref, err := alltransports.ParseImageName(ins.Name)
	if err != nil {
		return "", "", fmt.Errorf("Inspect: %w", err)
	}

	sysCtx := &types.SystemContext{
		DockerAuthConfig:            ins.DockerAuthConfig,
		ArchitectureChoice:          ins.OverrideArch,
		OSChoice:                    ins.OverrideOs,
		VariantChoice:               ins.OverrideVariant,
		DockerInsecureSkipTLSVerify: types.NewOptionalBool(ins.SkipTlsVerify),
	}
	source, err := ref.NewImageSource(ins.Ctx, sysCtx)
	if err != nil {
		return "", "", err
	}
	raw, mime, err := source.GetManifest(context.TODO(), nil)
	if err != nil {
		return "", "", err
	}
	img, err = image.FromUnparsedImage(
		ins.Ctx,
		sysCtx,
		image.UnparsedInstance(source, nil))
	if err != nil {
		return "", "", err
	}
	if ins.Raw {
		if ins.Config {
			var img types.Image

			config, err := img.ConfigBlob(ins.Ctx)
			if err != nil {
				return "", "", err
			}
			return string(config), "", nil
		}
		return string(raw), mime, nil
	}

	return "", "", nil
}
