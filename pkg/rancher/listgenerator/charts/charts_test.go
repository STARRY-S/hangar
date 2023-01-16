package charts

import (
	"os"
	"testing"

	"github.com/sirupsen/logrus"
)

func init() {
	logrus.SetLevel(logrus.DebugLevel)
}

func Test_fetchChartsFromPath(t *testing.T) {
	charts := Charts{
		RancherVersion: "v2.7.0",
		OS:             Linux,
		Type:           "",
		Path:           "test/pandaria-catalog",
		URL:            "",
		ImageSet:       make(map[string]map[string]bool),
	}
	err := charts.fetchChartsFromPath()
	if os.IsNotExist(err) {
		// skip if not exists
		return
	}
	if err != nil {
		t.Error(err)
	}
	for source := range charts.ImageSet {
		for value := range charts.ImageSet[source] {
			t.Logf("[%s] %s", source, value)
		}
	}
}
