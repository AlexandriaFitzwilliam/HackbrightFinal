function App() {
    const [shelves, setShelves] = React.useState({});

    return (
        <ReactRouterDOM.BrowserRouter>
            <div className="container-fluid">
                <ReactRouterDOM.Route exact path ="/">
                    <Homepage />
                </ReactRouterDOM.Route>
            </div>
        </ReactRouterDOM.BrowserRouter>
    );
}
ReactDOM.render(<App />, document.querySelector('#root'));