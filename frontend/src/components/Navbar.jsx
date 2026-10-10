import './Navbar.css';

function Navbar() {
  return (
    <header className="navbar">
      <a className="navbar-brand" href="/" aria-label="Hospital Room Radar home">
        <span className="navbar-logo" aria-hidden="true">
          <svg viewBox="0 0 24 24" role="img">
            <path d="M12 2.5 19 5v5.4c0 5-2.9 9.3-7 11.1-4.1-1.8-7-6.1-7-11.1V5l7-2.5Z" />
            <path d="M12 7v7M8.5 10.5h7" />
          </svg>
        </span>
        <span>Hospital Room Radar</span>
      </a>
    </header>
  );
}

export default Navbar;
