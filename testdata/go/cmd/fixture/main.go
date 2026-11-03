package main

import (
	"flag"
	"fmt"
	"os"

	"github.com/example/fixture/internal/version"
)

func main() {
	showVersion := flag.Bool("version", false, "print the version and exit")
	flag.Parse()

	if *showVersion {
		fmt.Println(version.String())
		return
	}
	fmt.Fprintln(os.Stderr, "fixture: nothing here yet")
}
