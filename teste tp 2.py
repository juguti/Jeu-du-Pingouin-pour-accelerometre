import matplotlib.pyplot as plt
import numpy as np

# ==========================================
# 1. PARAMÈTRES DES SYSTÈMES THÉORIQUES
# ==========================================
# Ordre 1 : H1(p) = K1 / (1 + p / omega_1)
K1 = 1.0  # Gain statique ordre 1
omega_1 = 10.0  # Pulsation de cassure ordre 1 (rad/s)

# Ordre 2 : H2(p) = K2 / (1 + 2*z/omega_0*p + p^2/omega_0^2)
K2 = 1.0  # Gain statique ordre 2
omega_0 = 100.0  # Pulsation propre ordre 2 (rad/s)
z = 0.5  # Facteur d'amortissement (pour information / repère)

# ==========================================
# 2. VOS POINTS EXPÉRIMENTAUX (À modifier)
# ==========================================
# Entrez ici vos fréquences/pulsations de mesure, gains (en dB) et phases (en degrés)
omega_exp = np.array([1, 5, 10, 50, 100, 500, 1000])  # en rad/s
gain_exp_dB = np.array(
    [0, -1, -3.5, -24, -42, -82, -122]
)  # Exemples de gains mesurés (dB)
phase_exp = np.array(
    [-5, -30, -55, -135, -185, -245, -270]
)  # Exemples de phases mesurées (degrés)

# ==========================================
# 3. CALCULS DES ASYMPTOTES THÉORIQUES
# ==========================================
# Plage de fréquences pour le tracé continu des courbes théoriques
omega = np.logspace(
    np.log10(omega_1 / 100), np.log10(omega_0 * 100), 1000
)


# Fonctions asymptotiques de l'Ordre 1
def gain_asymp_1(w):
  return 20 * np.log10(K1) - 20 * np.maximum(0, np.log10(w / omega_1))


def phase_asymp_1(w):
  return np.where(
      w < 0.1 * omega_1,
      0,
      np.where(
          w > 10 * omega_1, -90, -45 * (np.log10(w / (0.1 * omega_1)))
      ),
  )


# Fonctions asymptotiques de l'Ordre 2
def gain_asymp_2(w):
  return 20 * np.log10(K2) - 40 * np.maximum(0, np.log10(w / omega_0))


def phase_asymp_2(w):
  return np.where(
      w < 0.1 * omega_0,
      0,
      np.where(
          w > 10 * omega_0, -180, -90 * (np.log10(w / (0.1 * omega_0)))
      ),
  )


# Application aux vecteurs de fréquence
g1 = gain_asymp_1(omega)
p1 = phase_asymp_1(omega)

g2 = gain_asymp_2(omega)
p2 = phase_asymp_2(omega)

# Produit = Somme des amplitudes en dB et somme des phases
gain_total = g1 + g2
phase_total = p1 + p2

# ==========================================
# 4. DÉDUCTION DE L'ORDRE 2 À PARTIR DES POINTS EXPÉRIMENTAUX
# ==========================================
# On calcule la contribution théorique de l'ordre 1 aux fréquences de vos mesures
g1_exp = gain_asymp_1(omega_exp)
p1_exp = phase_asymp_1(omega_exp)

# Par déduction (Global = Ordre 1 + Ordre 2 => Ordre 2 = Global - Ordre 1)
gain_2_deduit_dB = gain_exp_dB - g1_exp
phase_2_deduit = phase_exp - p1_exp

# ==========================================
# 5. TRACÉ DES GRAPHIQUES
# ==========================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 9), sharex=True)

# --- Graphique du Gain ---
ax1.semilogx(
    omega, gain_total, 'b-', linewidth=2, label='Asymptote Totale (Théorique)'
)
ax1.semilogx(omega, g1, 'g--', label='Asymptote Ordre 1')
ax1.semilogx(omega, g2, 'r--', label='Asymptote Ordre 2')
ax1.semilogx(
    omega_exp,
    gain_exp_dB,
    'ko',
    markersize=7,
    label='Mesures Expérimentales (Total)',
)
ax1.semilogx(
    omega_exp,
    gain_2_deduit_dB,
    'rx',
    markersize=8,
    markeredgewidth=2,
    label="Points Ordre 2 (Déduits des mesures)",
)

ax1.set_ylabel('Gain (dB)', fontsize=12)
ax1.set_title(
    'Diagramme de Bode Asymptotique - Produit Ordre 1 $\times$ Ordre 2',
    fontsize=14,
)
ax1.grid(True, which='both', linestyle='--', alpha=0.7)
ax1.legend(loc='lower left')

# --- Graphique de la Phase ---
ax2.semilogx(
    omega, phase_total, 'b-', linewidth=2, label='Phase Totale (Théorique)'
)
ax2.semilogx(omega, p1, 'g--', label='Phase Ordre 1')
ax2.semilogx(omega, p2, 'r--', label='Phase Ordre 2')
ax2.semilogx(
    omega_exp,
    phase_exp,
    'ko',
    markersize=7,
    label='Mesures Expérimentales (Total)',
)
ax2.semilogx(
    omega_exp,
    phase_2_deduit,
    'rx',
    markersize=8,
    markeredgewidth=2,
    label="Points Ordre 2 (Déduits des mesures)",
)

ax2.set_xlabel('Pulsation $\omega$ (rad/s)', fontsize=12)
ax2.set_ylabel('Phase (degrés)', fontsize=12)
ax2.grid(True, which='both', linestyle='--', alpha=0.7)
ax2.legend(loc='lower left')

plt.tight_layout()
plt.show()