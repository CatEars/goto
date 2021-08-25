use dirs::config_dir;

pub fn get_config_dir() -> std::path::PathBuf {
    let mut shell_dir = config_dir().unwrap();
    shell_dir.push("goto-cd");
    shell_dir
}

pub fn get_config_toml_path(config_name: &str) -> std::path::PathBuf {
    let mut cfg = get_config_dir();
    cfg.push(format!("{}.toml", config_name));
    cfg
}

pub fn get_config_shell_dir() -> std::path::PathBuf {
    let mut shell_dir = get_config_dir();
    shell_dir.push("shell");
    shell_dir
}

pub fn get_config_script_path(shell_script_name: &str) -> std::path::PathBuf {
    let mut shell_path = get_config_shell_dir();
    shell_path.push(shell_script_name);
    shell_path
}

#[cfg(target_family = "windows")]
pub fn canonicalize_path(path: &std::path::PathBuf) -> std::path::PathBuf {
    dunce::canonicalize(path).unwrap()
}

#[cfg(target_family = "unix")]
pub fn canonicalize_path(path: &std::path::PathBuf) -> std::path::PathBuf {
    path.canonicalize().unwrap()
}