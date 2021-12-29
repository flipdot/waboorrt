module gitserver

go 1.16

require (
	github.com/go-redis/redis/v8 v8.11.4
	github.com/sosedoff/gitkit v0.3.0
)

replace github.com/sosedoff/gitkit v0.3.0 => github.com/phlmn/gitkit v0.3.1-0.20211229040720-d5e2cb15ed04
