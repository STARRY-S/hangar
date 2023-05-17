package skopeo_test

import (
	"os"
	"testing"

	"github.com/cnrancher/hangar/pkg/skopeo"
)

func Test_Installed(t *testing.T) {
	err := skopeo.Installed()
	if err != nil {
		if os.IsNotExist(err) {
			return
		}
		t.Error(err)
	}
}
