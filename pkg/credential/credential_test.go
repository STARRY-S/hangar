package credential_test

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/cnrancher/hangar/pkg/credential"
	"github.com/stretchr/testify/assert"
)

func Test_GetRegistryCredential(t *testing.T) {
	_, err := os.Stat(filepath.Join(os.Getenv("HOME"), ".docker/config.json"))
	if os.IsNotExist(err) {
		return
	}

	u, p, err := credential.GetRegistryCredential("")
	if err != nil {
		t.Error(err)
	}
	assert.NotEmpty(t, u)
	assert.NotEmpty(t, p)
}
