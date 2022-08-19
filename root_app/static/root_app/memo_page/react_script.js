const root = ReactDOM.createRoot(document.querySelector('#root'));

function Main() {
  return (
    <div>
      <h1>Hello, React!</h1>
      <p>Halaman ini akan dibuat menggunakan react.js (cdn)</p>
    </div>
  )
}

root.render(<Main />)