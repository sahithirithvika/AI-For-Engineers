import React, { useState, useEffect } from "react";

export default function Settings({ user, setTheme }) {
  const [open, setOpen] = useState(false);
  const [theme, setLocalTheme] = useState("light");
  const [notifications, setNotifications] = useState(true);

  // Fetch saved settings when modal opens
  useEffect(() => {
    if (open) {
      fetch(`http://localhost:5000/settings/${user}`)
        .then(res => res.json())
        .then(data => {
          setLocalTheme(data.theme);
          setNotifications(data.notifications);
        });
    }
  }, [open, user]);

  const saveSettings = async () => {
    await fetch(`http://localhost:5000/settings/${user}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ theme, notifications })
    });
    alert("Settings saved!");
    setTheme(theme); // ✅ apply theme immediately
    setOpen(false);
  };

  return (
    <>
      <button onClick={() => setOpen(true)} style={{ position: "absolute", bottom: 10, left: 10 }}>
        ⚙ Settings
      </button>

      {open && (
        <div style={{
          position: "fixed", top: "20%", left: "30%", background: "#fff",
          padding: "20px", border: "1px solid #ccc", borderRadius: "8px"
        }}>
          <h3>Settings</h3>

          <label>
            Theme:
            <select value={theme} onChange={e => setLocalTheme(e.target.value)}>
              <option value="light">Light</option>
              <option value="dark">Dark</option>
            </select>
          </label>

          <br /><br />

          <label>
            Notifications:
            <input
              type="checkbox"
              checked={notifications}
              onChange={e => setNotifications(e.target.checked)}
            />
          </label>

          <br /><br />

          <button onClick={saveSettings}>Save</button>
          <button onClick={() => setOpen(false)}>Close</button>
        </div>
      )}
    </>
  );
}
