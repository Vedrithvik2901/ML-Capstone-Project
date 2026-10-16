
<template>
  <main class="home-page">
    <!-- Navigation -->
    <header class="navbar">
      <div class="brand">
        <span class="brand-icon">ML</span>
        <span>Capstone Explorer</span>
      </div>

      <nav class="nav-links">
        <RouterLink to="/" class="nav-link active">
          Home
        </RouterLink>

        <RouterLink to="/datasets" class="nav-link">
          Datasets
        </RouterLink>
      </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <span class="eyebrow">
          MACHINE LEARNING PROJECT
        </span>

        <h1>
          Explore data.<br />
          Understand models.<br />
          <span class="highlight">Discover insights.</span>
        </h1>

        <p class="hero-description">
          An interactive platform to explore machine learning
          datasets, understand algorithms, and compare model
          performance across different learning tasks.
        </p>

        <div class="hero-actions">
          <RouterLink to="/datasets" class="primary-button">
            Explore Datasets
            <span>→</span>
          </RouterLink>

          <a href="#tracks" class="secondary-button">
            Explore ML Tracks
          </a>
        </div>
      </div>

      <div class="hero-visual">
        <div class="visual-card">
          <div class="visual-header">
            <span class="visual-dot"></span>
            <span>ML WORKSPACE</span>
          </div>

          <div class="chart-area">
            <div class="chart-label">MODEL PERFORMANCE</div>

            <div class="chart-bars">
              <div class="bar bar-1"></div>
              <div class="bar bar-2"></div>
              <div class="bar bar-3"></div>
              <div class="bar bar-4"></div>
              <div class="bar bar-5"></div>
              <div class="bar bar-6"></div>
            </div>

            <div class="chart-footer">
              <span>Dataset Analysis</span>
              <span class="chart-status">Ready to explore</span>
            </div>
          </div>

          <div class="visual-bottom">
            <div class="visual-stat">
              <span class="stat-icon">01</span>
              <div>
                <strong>Classification</strong>
                <small>Predict categories</small>
              </div>
            </div>

            <div class="visual-stat">
              <span class="stat-icon">02</span>
              <div>
                <strong>Regression</strong>
                <small>Predict values</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Machine Learning Tracks -->
    <section id="tracks" class="tracks-section">
      <div class="section-heading">
        <div>
          <span class="eyebrow">YOUR WORKSPACE</span>
          <h2>Explore machine learning</h2>
        </div>

        <p>
          Start with a dataset, explore a learning task,
          and move towards understanding the models.
        </p>
      </div>

      <div class="track-grid">
      <article class="track-card">
        <div class="track-number">01</div>
        <div class="track-icon classification-icon">C</div>
        <h3>Classification</h3>
        <p>
          Explore datasets used to predict discrete
          categories and class labels.
        </p>
        <RouterLink to="/datasets" class="track-link">
          Explore datasets <span>→</span>
        </RouterLink>
      </article>

      <article class="track-card">
        <div class="track-number">02</div>
        <div class="track-icon regression-icon">R</div>
        <h3>Regression</h3>
        <p>
          Discover datasets for predicting continuous
          numerical values.
        </p>
        <RouterLink to="/datasets" class="track-link">
          Explore datasets <span>→</span>
        </RouterLink>
      </article>

      <article class="track-card">
        <div class="track-number">03</div>
        <div class="track-icon clustering-icon">K</div>
        <h3>Clustering</h3>
        <p>
          Investigate datasets for discovering patterns
          and grouping similar observations.
        </p>
        <RouterLink to="/datasets" class="track-link">
          Explore datasets <span>→</span>
        </RouterLink>
      </article>
      </div>
    </section>

    <!-- Footer -->
    <footer class="home-footer">
      <span>ML Capstone Explorer</span>
      <span>Explore · Learn · Analyze</span>
    </footer>
  </main>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
  background: #111318;
  color: #f3f4f6;
  font-family: Inter, Arial, sans-serif;
  padding: 0 7%;
}

.navbar {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #292c33;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 17px;
  font-weight: 700;
}

.brand-icon {
  background: #a3e635;
  color: #111318;
  padding: 9px;
  border-radius: 9px;
  font-size: 14px;
}

.nav-links {
  display: flex;
  gap: 30px;
}

.nav-link {
  color: #a0a3ad;
  text-decoration: none;
  font-size: 14px;
}

.nav-link:hover,
.nav-link.active {
  color: #a3e635;
}

.hero {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  align-items: center;
  gap: 60px;
  padding: 90px 0;
}

.eyebrow {
  color: #a3e635;
  font-size: 11px;
  letter-spacing: 2px;
  font-weight: 700;
}

.hero h1 {
  font-size: clamp(42px, 5vw, 68px);
  line-height: 1.1;
  letter-spacing: -2px;
  margin: 25px 0;
}

.highlight {
  color: #a3e635;
}

.hero-description {
  max-width: 500px;
  color: #a0a3ad;
  font-size: 16px;
  line-height: 1.8;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-top: 35px;
}

.primary-button,
.secondary-button {
  padding: 14px 20px;
  border-radius: 8px;
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
}

.primary-button {
  background: #a3e635;
  color: #111318;
}

.primary-button span {
  margin-left: 12px;
}

.secondary-button {
  border: 1px solid #373a42;
  color: #f3f4f6;
}

.visual-card {
  background: #1b1e24;
  border: 1px solid #30333b;
  border-radius: 18px;
  padding: 25px;
}

.visual-header {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #a0a3ad;
  font-size: 11px;
  letter-spacing: 1px;
}

.visual-dot {
  width: 8px;
  height: 8px;
  background: #a3e635;
  border-radius: 50%;
}

.chart-area {
  background: #14161b;
  border-radius: 12px;
  padding: 22px;
  margin-top: 25px;
}

.chart-label {
  color: #a0a3ad;
  font-size: 11px;
  letter-spacing: 1px;
}

.chart-bars {
  height: 180px;
  display: flex;
  align-items: end;
  justify-content: space-around;
  gap: 12px;
  border-bottom: 1px solid #343741;
  margin: 20px 0;
}

.bar {
  width: 12%;
  background: #a3e635;
  border-radius: 5px 5px 0 0;
}

.bar-1 { height: 40%; opacity: 0.4; }
.bar-2 { height: 65%; opacity: 0.6; }
.bar-3 { height: 50%; opacity: 0.5; }
.bar-4 { height: 85%; }
.bar-5 { height: 70%; opacity: 0.8; }
.bar-6 { height: 95%; }

.chart-footer {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #a0a3ad;
}

.chart-status {
  color: #a3e635;
}

.visual-bottom {
  display: flex;
  gap: 15px;
  margin-top: 20px;
}

.visual-stat {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #14161b;
  padding: 14px;
  border-radius: 10px;
  flex: 1;
}

.stat-icon {
  color: #a3e635;
  font-size: 12px;
}

.visual-stat strong,
.visual-stat small {
  display: block;
}

.visual-stat strong {
  font-size: 12px;
}

.visual-stat small {
  color: #a0a3ad;
  font-size: 10px;
  margin-top: 5px;
}

.tracks-section {
  padding: 40px 0 80px;
}

.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 30px;
  margin-bottom: 35px;
}

.section-heading h2 {
  font-size: 32px;
  margin: 12px 0 0;
}

.section-heading > p {
  color: #a0a3ad;
  max-width: 380px;
  line-height: 1.7;
  font-size: 14px;
}

.track-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.track-card {
  position: relative;
  background: #1b1e24;
  border: 1px solid #30333b;
  border-radius: 14px;
  padding: 25px;
}

.track-number {
  position: absolute;
  top: 25px;
  right: 25px;
  color: #666975;
  font-size: 12px;
}

.track-icon {
  width: 45px;
  height: 45px;
  display: grid;
  place-items: center;
  border-radius: 10px;
  font-weight: 700;
  font-size: 18px;
}

.classification-icon {
  background: #273c27;
  color: #a3e635;
}

.regression-icon {
  background: #28364b;
  color: #82b4ff;
}

.clustering-icon {
  background: #3d3046;
  color: #c69aff;
}

.track-card h3 {
  margin-top: 25px;
  font-size: 20px;
}

.track-card p {
  color: #a0a3ad;
  font-size: 14px;
  line-height: 1.7;
  min-height: 70px;
}

.track-link {
  display: inline-flex;
  justify-content: space-between;
  gap: 12px;
  margin-top: 15px;
  color: #a3e635;
  text-decoration: none;
  font-size: 13px;
  font-weight: 600;
}

.home-footer {
  display: flex;
  justify-content: space-between;
  border-top: 1px solid #292c33;
  padding: 25px 0;
  color: #777b86;
  font-size: 12px;
}

@media (max-width: 900px) {
  .hero {
    grid-template-columns: 1fr;
    padding: 60px 0;
  }

  .track-grid {
    grid-template-columns: 1fr;
  }

  .section-heading {
    align-items: start;
    flex-direction: column;
  }
}

@media (max-width: 500px) {
  .home-page {
    padding: 0 5%;
  }

  .navbar {
    height: 70px;
  }

  .brand {
    font-size: 14px;
  }

  .nav-links {
    gap: 15px;
  }

  .hero h1 {
    font-size: 42px;
  }

  .visual-bottom {
    flex-direction: column;
  }

  .home-footer {
    gap: 15px;
    flex-direction: column;
  }
}
</style>
