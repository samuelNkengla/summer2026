import { useEffect, useState } from "react";
import { BrowserRouter, Link, Route, Routes, useParams } from "react-router-dom";
import "./App.css";

const API_URL = "";

function Page() {
  const { slug = "home" } = useParams();
  const [page, setPage] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API_URL}/api/pages/${slug}`)
      .then((response) => {
        if (!response.ok) throw new Error("Could not load page");
        return response.json();
      })
      .then(setPage)
      .catch((err) => setError(err.message));
  }, [slug]);

  async function handleAction() {
    if (!page) return;

    await fetch(`${API_URL}/api/events/button-click`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        page_slug: page.slug,
        button_label: page.button_label,
      }),
    });

    if (page.button_url.startsWith("/")) {
      window.location.href = page.button_url;
    } else {
      window.open(page.button_url, "_blank");
    }
  }

  if (error) return <p>{error}</p>;
  if (!page) return <p>Loading…</p>;

  return (
    <main>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
      </nav>

      <section className="hero">
        <img src={page.image_url} alt="" />
        <div>
          <h1>{page.title}</h1>
          <p>{page.body}</p>
          <button onClick={handleAction}>{page.button_label}</button>
        </div>
      </section>
    </main>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Page />} />
        <Route path="/about" element={<Page />} />
      </Routes>
    </BrowserRouter>
  );
}