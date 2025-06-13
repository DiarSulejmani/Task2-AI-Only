import React, { useState } from 'react';

const TABS = ['Multiple Choice', 'True/False', 'Fill in the Blank'];

const CreateQuestions: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>(TABS[0]);

  return (
    <div>
      <h1>Create Questions</h1>
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
        {TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              padding: '.5rem 1rem',
              background: activeTab === tab ? '#61dafb' : '#eee',
            }}
          >
            {tab}
          </button>
        ))}
      </div>
      <p>Selected Tab: {activeTab}</p>
      {/* TODO: Implement question forms for each tab */}
    </div>
  );
};

export default CreateQuestions;
