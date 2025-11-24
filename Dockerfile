# ==============================================================================
# 1. BASE IMAGE: NVIDIA CUDA
# We use a base image that already includes CUDA and Python, which is crucial
# for performance on the RTX 4060.
# Recommended: cuda:12.1.1-devel-ubuntu22.04 or similar.
# "devel" includes compilation tools that might be necessary
# for vLLM or some PyTorch/Transformers dependencies.
# ==============================================================================
FROM nvidia/cuda:12.0.0-base-ubuntu22.04

# Sets environment variables for non-interactive execution and key paths
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Europe/Madrid \
    LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TERM=xterm \
    HOME=/root

WORKDIR /requirements
COPY requirements /requirements

# ==============================================================================
# 2. SYSTEM DEPENDENCIES INSTALLATION
# ==============================================================================
RUN apt-get update && apt-get upgrade -y && \
    # base
    apt install -y git wget make curl unzip zstd \
    # extras
    figlet bat btop \
    # iputils-ping \
    # python3
    python3-pip python3-dev  && \
    # Ensure that 'python' points to python3
    update-alternatives --install /usr/bin/python python /usr/bin/python3 1 && \
    # timezone
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    install -m 0755 -d /etc/apt/keyrings && \
    # docker
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y --no-install-recommends docker-ce-cli docker-compose-plugin \
    # agents
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt install -y nodejs \
    # clean
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apk/* \
    && rm -rf /tmp/* \
    # config
    echo "sh /scripts/welcome.sh" >> ~/.zshrc && \
    echo "sh /scripts/welcome.sh" >> ~/.bashrc

RUN pip install --no-cache-dir -r /requirements/base.txt

# ============= ZSH CONFIGURATION =============
RUN apt-get update && apt-get install -y zsh && \
    sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" -- \
    -t aussiegeek && \
    wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true && \
    echo "alias wisrovi='echo \"https://es.linkedin.com/in/wisrovi-rodriguez\"'" >> ~/.zshrc && \
    echo "git config --global user.name 'wisrovi'" >> ~/.zshrc && \
    echo "git config --global user.email 'wisrovi.rodriguez@gmail.com'" >> ~/.zshrc

RUN git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting && \
    git clone https://github.com/zsh-users/zsh-completions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-completions && \
    sed -i '/^plugins=/s/)/ zsh-autosuggestions zsh-syntax-highlighting zsh-completions z docker docker-compose)/' ~/.zshrc && \
    echo "alias cat='batcat'" >> ~/.zshrc && \
    echo "alias nano='edit'" >> ~/.zshrc && \
    echo "alias help='sh /scripts/welcome.sh'" >> ~/.zshrc && \
    echo /bin/zsh >> /etc/shells


# ============= OPENCODE =============
RUN curl -fsSL https://opencode.ai/install | bash
ENV PATH="/root/.opencode/bin:/usr/local/bin:$PATH"

# ============= MICROSOFT EDIT =============
RUN wget https://github.com/microsoft/edit/releases/download/v1.2.1/edit-1.2.0-x86_64-linux-gnu.tar.zst && \
    tar -I zstd -xf edit-1.2.0-x86_64-linux-gnu.tar.zst && \
    mv edit /usr/local/bin/edit && \
    rm edit-1.2.0-x86_64-linux-gnu.tar.zst && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get autoremove -y && \
    apt-get autoclean && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /root/.cache/* /root/.npm && \
    echo "wAgents" > /etc/hostname

WORKDIR /scripts
COPY scripts /scripts
RUN chmod +x -R /scripts


WORKDIR /python_test
COPY python /python_test

# ============= EXTRA TOOLS INSTALLATION =============
# 1. APT Installs
# exa, ripgrep, fd (fd-find), duf, trash-cli, httpie, rsync, datamash (datemask), pydf
# Remove docker repo to avoid network timeouts during update
RUN rm /etc/apt/sources.list.d/docker.list

RUN apt-get update && apt-get install -y --fix-missing \
    iputils-ping \
    htop \
    libncurses5-dev \
    libncursesw5-dev \
    exa \
    ripgrep \
    fd-find \
    duf \
    trash-cli \
    httpie \
    rsync \
    datamash \
    pydf \
    && rm -rf /var/lib/apt/lists/*

# 2. Manual Installs (Binaries not in APT or outdated)

# Lazydocker
RUN wget https://github.com/jesseduffield/lazydocker/releases/download/v0.23.3/lazydocker_0.23.3_Linux_x86_64.tar.gz && \
    tar -xvf lazydocker_0.23.3_Linux_x86_64.tar.gz && \
    mv lazydocker /usr/local/bin/lazydocker && \
    rm lazydocker_0.23.3_Linux_x86_64.tar.gz

# Broot (Directory tree)
RUN wget https://dystroy.org/broot/download/x86_64-linux/broot -O /usr/local/bin/broot && \
    chmod +x /usr/local/bin/broot

# Zoxide (Smart cd)
RUN curl -sS https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | bash -s -- --bin-dir /usr/local/bin

# Dust (Better du)
RUN wget https://github.com/bootandy/dust/releases/download/v0.8.6/dust-v0.8.6-x86_64-unknown-linux-musl.tar.gz && \
    tar -xvf dust-v0.8.6-x86_64-unknown-linux-musl.tar.gz && \
    mv dust-v0.8.6-x86_64-unknown-linux-musl/dust /usr/local/bin/dust && \
    rm -rf dust-v0.8.6-x86_64-unknown-linux-musl*

# Procs (Better ps)
RUN wget https://github.com/dalance/procs/releases/download/v0.14.0/procs-v0.14.0-x86_64-linux.zip && \
    unzip procs-v0.14.0-x86_64-linux.zip && \
    mv procs /usr/local/bin/procs && \
    rm procs-v0.14.0-x86_64-linux.zip

# Gping (Graphical ping)
RUN wget https://github.com/orf/gping/releases/download/gping-v1.16.0/gping-Linux-x86_64.tar.gz && \
    tar -xvf gping-Linux-x86_64.tar.gz && \
    mv gping /usr/local/bin/gping && \
    rm gping-Linux-x86_64.tar.gz

# Dijo (Habit tracker) - Installed via cargo
RUN apt-get update && apt-get install -y cargo && \
    cargo install --locked dijo && \
    mv /root/.cargo/bin/dijo /usr/local/bin/dijo && \
    apt-get remove -y cargo && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* /root/.cargo && \
    mkdir -p /root/.config/dijo /root/.local/share/dijo && \
    echo "[]" > /root/.local/share/dijo/dijo.json

ENV TERM=xterm-256color

# 3. ZSH Configuration & Aliases
RUN echo 'eval "$(zoxide init zsh)"' >> ~/.zshrc && \
    echo 'eval "$(broot --print-shell-function zsh)"' >> ~/.zshrc && \
    echo "alias ls='exa --icons'" >> ~/.zshrc && \
    echo "alias ll='exa -l --icons'" >> ~/.zshrc && \
    echo "alias la='exa -la --icons'" >> ~/.zshrc && \
    echo "alias cd='z'" >> ~/.zshrc && \
    echo "alias grep='rg'" >> ~/.zshrc && \
    echo "alias find='fd'" >> ~/.zshrc && \
    echo "alias du='dust'" >> ~/.zshrc && \
    echo "alias df='duf'" >> ~/.zshrc && \
    echo "alias ps='procs'" >> ~/.zshrc && \
    echo "alias ping='gping'" >> ~/.zshrc && \
    echo "alias top='btop'" >> ~/.zshrc && \
    echo "alias tree='broot'" >> ~/.zshrc && \
    echo "alias rm='trash-put'" >> ~/.zshrc

WORKDIR /app


SHELL [ "zsh" ]

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD (opencode --version && nvidia-smi) || exit 1

CMD ["tail", "-f", "/dev/null"]

