import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

def normal(x, mu, sigma):
    return np.exp(-(x - mu) ** 2 / (2 * sigma)) / np.sqrt(2 * np.pi * sigma)

def plot_standard_normal_df():
    fig, ax = plt.subplots(figsize=(8, 6))

    step = 0.01
    x_min = -4
    x_max = 4
    mu = 0
    sigma = 1
    x = np.arange(x_min, x_max, step)
    ax.plot(x, normal(x, mu, sigma), color='blue')
    ax.set_xlim(-4, 4)
    ax.set_ylim(0, 0.5)
    plt.show()
    fig.savefig('standard_normal_df')

def plot_normal_df_mean(mu, sigma, ax):
    step = 0.01
    x_min = -4
    x_max = 4
    x = np.arange(x_min, x_max, step)
    ax.plot(x, normal(x, mu, sigma), color='blue')
    ax.vlines(x=mu, ymin=0, ymax=normal(mu, mu, sigma), color='red')
    minus_sigma = mu - sigma
    ax.vlines(x=minus_sigma, ymin=0, ymax=normal(minus_sigma, mu, sigma), color='green')
    plus_sigma = mu + sigma
    ax.vlines(x=plus_sigma, ymin=0, ymax=normal(plus_sigma, mu, sigma), color='green')
    ax.set_xlim(-4, 4)
    ax.set_ylim(0, 0.6)
    ax.text(2, 0.5, f'μ = {mu}', color='red', size='xx-large')
    ax.text(2, 0.45, f'Σ = {sigma}', color='green', size='xx-large')

def plot_normal_df_variance(mu, sigma, ax):
    step = 0.01
    x_min = -4
    x_max = 4
    x = np.arange(x_min, x_max, step)
    ax.plot(x, normal(x, mu, sigma), color='blue')
    ax.vlines(x=mu, ymin=0, ymax=normal(mu, mu, sigma), color='red')
    minus_sigma = mu - sigma
    ax.vlines(x=minus_sigma, ymin=0, ymax=normal(minus_sigma, mu, sigma), color='green')
    plus_sigma = mu + sigma
    ax.vlines(x=plus_sigma, ymin=0, ymax=normal(plus_sigma, mu, sigma), color='green')
    ax.set_xlim(-4, 4)
    ax.set_ylim(0, 0.6)
    ax.text(2, 0.5, f'μ = {mu}', color='red', size='xx-large')
    ax.text(2, 0.45, f'Σ = {sigma}', color='green', size='xx-large')

def plot_normal_df_mean_variance(i, mean_mu, mean_sigma, var_mu, var_sigma, ax1, ax2):
    ax1.cla()
    ax2.cla()
    plot_normal_df_mean(mean_mu[i], mean_sigma[i], ax1)
    plot_normal_df_variance(var_mu[i], var_sigma[i], ax2)

def plot_normal_df_mean_variance_animation():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 12))

    mean_mu_array = np.array([-1.0, .0, 1.0])
    mean_sigma_array = np.array([1.0, 1.0, 1.0])
    var_mu_array = np.array([.0, .0, .0])
    var_sigma_array = np.array([0.5, 1.0, 2.0])

    a = animation.FuncAnimation(fig, plot_normal_df_mean_variance, fargs=(mean_mu_array, mean_sigma_array, var_mu_array, var_sigma_array, ax1, ax2), interval=2000, frames=3)
    a.save('normal_df_mean_variance_animation.gif')

def plot_normal_df_prob():
    fig, ax = plt.subplots(figsize=(8, 6))

    step = 0.01
    x_min = -4
    x_max = 4
    r_min = -1
    r_max = 2
    mu = 0
    sigma = 1
    r = np.arange(r_min, r_max, step)
    ax.fill_between(r, 0, normal(r, mu, sigma), fc='yellow')
    ax.vlines(x=r_min, ymin=0, ymax=normal(r_min, mu, sigma), color='gray')
    ax.vlines(x=r_max, ymin=0, ymax=normal(r_max, mu, sigma), color='gray')
    x = np.arange(x_min, x_max, step)
    ax.plot(x, normal(x, mu, sigma), color='blue')
    ax.set_xlim(-4, 4)
    ax.set_ylim(0, 0.5)
    plt.show()
    fig.savefig('normal_df_prob')

plot_standard_normal_df()
plot_normal_df_mean_variance_animation()
plot_normal_df_prob()
