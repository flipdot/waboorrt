package waboorrt

import (
	"fmt"
	"net/http"

	"github.com/gorilla/rpc/v2"
	"github.com/gorilla/rpc/v2/json2"
	"github.com/stoewer/go-strcase"
)

type customCodec struct {
	rpc.Codec
}

func newCustomCodec() *customCodec {
	return &customCodec{
		json2.NewCodec(),
	}
}

func (c *customCodec) NewRequest(r *http.Request) rpc.CodecRequest {
	return &customCodecRequest{
		CodecRequest: c.Codec.NewRequest(r),
	}
}

type customCodecRequest struct {
	rpc.CodecRequest
}

func (c *customCodecRequest) Method() (string, error) {
	m, err := c.CodecRequest.Method()
	if err != nil {
		return "", err
	}

	return fmt.Sprintf("Bot.%s", strcase.UpperCamelCase(m)), nil
}
