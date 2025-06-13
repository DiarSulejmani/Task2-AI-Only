import React from 'react';

export default function CreateQuestions() {
  return (
    <div>
      <h2>Create Questions</h2>
      <ul className="nav nav-tabs mb-3" role="tablist">
        <li className="nav-item" role="presentation"><button className="nav-link active" id="auto-tab" data-bs-toggle="tab" data-bs-target="#auto" type="button" role="tab">Automated</button></li>
        <li className="nav-item" role="presentation"><button className="nav-link" id="semi-tab" data-bs-toggle="tab" data-bs-target="#semi" type="button" role="tab">Semi-Automated</button></li>
        <li className="nav-item" role="presentation"><button className="nav-link" id="manual-tab" data-bs-toggle="tab" data-bs-target="#manual" type="button" role="tab">Manual</button></li>
      </ul>
      <div className="tab-content">
        <div className="tab-pane fade show active" id="auto" role="tabpanel"><h3>Automated Question Generation</h3></div>
        <div className="tab-pane fade" id="semi" role="tabpanel"><h3>Semi-Automated Question Generation</h3></div>
        <div className="tab-pane fade" id="manual" role="tabpanel"><h3>Manual Question Creation</h3></div>
      </div>
    </div>
  );
}
