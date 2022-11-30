package main

import (
	"fmt"
	"log"
	"net/http"
	"time"

	tea "github.com/charmbracelet/bubbletea"
)

const baseurl = "https://www.tabnews.com.br/api/v1/"

type request struct {
	status int
	err    error
}

var exiting bool = false

type statusMsg int

type errMsg struct{ error }

var client = &http.Client{
	Timeout: 10 * time.Second,
}

func (e errMsg) Error() string { return e.error.Error() }

func main() {
	p := tea.NewProgram(request{}, tea.WithAltScreen())
	if _, err := p.Run(); err != nil {
		log.Fatal(err)
	}
}

func (r request) Init() tea.Cmd {
	return checkServer
}

func (r request) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "q", "ctrl+c", "esc":
			exiting = true
			return r, tea.Quit
		default:
			return r, nil
		}

	case statusMsg:
		r.status = int(msg)
		exiting = true
		return r, tea.Quit

	case errMsg:
		r.err = msg
		return r, nil

	default:
		return r, nil
	}
}

func (r request) View() string {
	view := getResults("users/filipedeschamps")
	view += "\n teste"

	if exiting {
		return "Fechando o programa..."
	}

	return view
}

func getResults(p string) string {
	res, err := client.Get(baseurl + p)

	if err != nil {
		return err.Error()
	}

	defer res.Body.Close()

	return ""
}

func checkServer() tea.Msg {
	s := fmt.Sprintf("Checking %s...", baseurl)

	res, err := client.Get(baseurl + "users/filipedeschamps")

	if err != nil {
		s += fmt.Sprintf("something went wrong: %s", err)
	} else if res.StatusCode != 0 {
		s += fmt.Sprintf("%d %s", res.StatusCode, http.StatusText(res.StatusCode))
	}

	if err != nil {
		return errMsg{err}
	}

	defer res.Body.Close()

	return res.StatusCode

}
