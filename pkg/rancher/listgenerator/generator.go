package listgenerator

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"sort"
	"strings"
	"time"

	"github.com/cnrancher/image-tools/pkg/utils"
	"github.com/rancher/rke/types/kdm"
	"golang.org/x/mod/semver"
)

// Generator is a generator to generate image list from charts, KDM data, etc.
type Generator struct {
	RancherVersion string // rancher version

	ChartsPaths []string // the paths of chart repo in local dir
	ChartURLs   []string // remote URLs of charts repo

	KDMPath string // the path of KDM data.json file
	KDMURL  string // the remote URL of KDM data.json

	WindowsImageArguments []string
	LinuxImageArguments   []string

	// generated images, map[source]map[image-name]true
	GeneratedLinuxImages   map[string]map[string]bool
	GeneratedWindowsImages map[string]map[string]bool
}

func (g *Generator) init() {
	if g.GeneratedLinuxImages == nil {
		g.GeneratedLinuxImages = make(map[string]map[string]bool)
	}
	if g.GeneratedWindowsImages == nil {
		g.GeneratedWindowsImages = make(map[string]map[string]bool)
	}
}

func (g *Generator) selfCheck() error {
	if g.RancherVersion == "" {
		return fmt.Errorf("RancherVersion is empty")
	}
	if !strings.HasPrefix(g.RancherVersion, "v") {
		g.RancherVersion = "v" + g.RancherVersion
	}
	if !semver.IsValid(g.RancherVersion) {
		return fmt.Errorf("%q is not a valid version", g.RancherVersion)
	}
	if g.ChartURLs == nil && g.ChartsPaths == nil &&
		g.KDMPath == "" && g.KDMURL == "" {
		return fmt.Errorf("no input source provided")
	}

	return nil
}

func (g *Generator) Generate() error {
	if err := g.selfCheck(); err != nil {
		return err
	}
	g.init()

	if err := g.generateFromChartPaths(); err != nil {
		return err
	}

	if err := g.generateFromChartURLs(); err != nil {
		return err
	}

	if err := g.generateFromKDMPath(); err != nil {
		return err
	}

	if err := g.generateFromKDMURL(); err != nil {
		return err
	}

	if err := g.handleImageArguments(); err != nil {
		return err
	}

	return nil
}

func (g *Generator) generateFromChartPaths() error {
	if g.ChartsPaths == nil || len(g.ChartsPaths) == 0 {
		return nil
	}
	return nil
}

func (g *Generator) generateFromChartURLs() error {
	if g.ChartURLs == nil || len(g.ChartURLs) == 0 {
		return nil
	}
	return nil
}

func (g *Generator) generateFromKDMPath() error {
	if g.KDMPath == "" {
		return nil
	}
	b, err := os.ReadFile(g.KDMPath)
	if err != nil {
		return fmt.Errorf("generateFromKDMPath: %w", err)
	}
	return g.generateFromKDMData(b)
}

func (g *Generator) generateFromKDMURL() error {
	if g.KDMURL == "" {
		return nil
	}
	client := http.Client{
		Timeout: 5 * time.Second,
	}
	resp, err := client.Get(g.KDMURL)
	if err != nil {
		return fmt.Errorf("generateFromKDMURL: %w", err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != 200 {
		return fmt.Errorf("generateFromKDMURL: get url [%q]: %v",
			g.KDMURL, resp.Status)
	}
	b, err := io.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("generateFromKDMURL: %w", err)
	}
	return g.generateFromKDMData(b)
}

func (g *Generator) generateFromKDMData(b []byte) error {
	data, err := kdm.FromData(b)
	if err != nil {
		return fmt.Errorf("generateFromKDMData: %w", err)
	}
	// get k3s/rke2 upgrade images
	eg := UpgradeGenerator{
		Source:         K3S,
		RancherVersion: g.RancherVersion,
		MinKubeVersion: "v1.21.0",
		Data:           data.K3S,
	}
	k3sUpgradeImages, err := eg.GetImages()
	if err != nil {
		return fmt.Errorf("generateFromKDMData: %w", err)
	}
	sort.Strings(k3sUpgradeImages)

	utils.DeleteIfExist("k3sUpgrade.txt")
	for _, l := range k3sUpgradeImages {
		// TODO: test purpose
		utils.AppendFileLine("k3sUpgrade.txt", l)
		if g.GeneratedLinuxImages["k3sUpgrade"] == nil {
			g.GeneratedLinuxImages["k3sUpgrade"] = make(map[string]bool)
		}
		g.GeneratedLinuxImages["k3sUpgrade"][l] = true
	}

	eg.Source = RKE2
	eg.Data = data.RKE2
	rke2UpgradeImages, err := eg.GetImages()
	if err != nil {
		return fmt.Errorf("generateFromKDMData: %w", err)
	}
	sort.Strings(rke2UpgradeImages)
	utils.DeleteIfExist("rke2All.txt")
	for _, l := range rke2UpgradeImages {
		// TODO: test purpose
		utils.AppendFileLine("rke2All.txt", l)
		if g.GeneratedLinuxImages["rke2All"] == nil {
			g.GeneratedLinuxImages["rke2All"] = make(map[string]bool)
		}
		g.GeneratedLinuxImages["rke2All"][l] = true
	}

	return nil
}

func (g *Generator) handleImageArguments() error {
	return nil
}
