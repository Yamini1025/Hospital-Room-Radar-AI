import Dashboard from './components/Dashboard.jsx';
import './App.css';
import Footer from './components/Footer.jsx';
import Navbar from './components/Navbar.jsx';

function App() {
  return (
    <div className="app-shell">
      <Navbar />

      <main className="app">
        <Dashboard />
      </main>

      <Footer />
    </div>
  );
}

export default App;