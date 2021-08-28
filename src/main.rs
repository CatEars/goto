extern crate term;

mod storage;
mod embedded;
mod paths;
use clap::{App, Arg};
use std::cmp::max;
use storage::{ensure_directory_structure, get_current_profile};

fn parse_opts<'a, 'b>() -> clap::App<'a, 'b> {
    return App::new("Goto")
        .version("2.0.0")
        .author("'CatEars' <catears13@gmail.com>")
        .about("Give your terminal teleporting powers")
        .arg(
            Arg::with_name("add")
                .short("a")
                .long("add")
                .help("Add a new teleport to the current profile")
                .takes_value(true),
        )
        .arg(
            Arg::with_name("get")
                .short("g")
                .long("get")
                .help("Print a teleport target.")
                .takes_value(true),
        )
        .arg(
            Arg::with_name("prefix")
                .long("prefix")
                .help("List all targets that have X as prefix")
                .takes_value(true),
        )
        .arg(
            Arg::with_name("remove")
                .short("r")
                .long("remove")
                .help("Remove a teleport from the current profile")
                .takes_value(true),
        )
        .arg(
            Arg::with_name("list")
                .short("l")
                .long("list")
                .help("Lists all teleports")
                .takes_value(false),
        )
        .arg(
            Arg::with_name("install")
                .long("install")
                .help("Installs `goto` function into linux shell.")
                .takes_value(false),
        )
        .arg(
            Arg::with_name("install-powershell")
                .long("install-powershell")
                .help("Installs `goto` function into powershell")
                .takes_value(false),
        )
        .arg(
            Arg::with_name("config-dir")
                .long("config-dir")
                .help("Prints the directory where goto configuration is stored")
                .takes_value(false)
        );

}

fn list_profile() {
    let msg = "Need access to the terminal, but couldn't get that";
    let mut t = term::stdout().expect(msg);

    let profile = get_current_profile().unwrap();
    let max_key_length = profile.keys().map(|x| x.len()).fold(0, |a, b| max(a, b));

    for k in profile.keys() {
        t.fg(term::color::GREEN).unwrap();
        write!(t, "{:<width$}", k, width = max_key_length + 1).unwrap();
        t.fg(term::color::WHITE).unwrap();
        write!(t, " -> ").unwrap();
        t.fg(term::color::GREEN).unwrap();
        let x = profile[k].as_str().unwrap();
        writeln!(t, "{}", x).unwrap();
    }

    t.reset().unwrap();
}

fn get_from_profile(key: &str) {
    let mut t = term::stdout().unwrap();

    let mut real_key = String::from(key);
    if real_key.ends_with("/") {
        real_key.pop();
    }

    let profile = get_current_profile().unwrap();
    let ans = profile.get(&real_key);

    match ans {
        Some(x) => {
            let v = x.as_str().unwrap();
            writeln!(t, "{}", v).unwrap();
        }
        _ => {
            t.fg(term::color::RED).unwrap();
            writeln!(t, "{} is not a valid teleport.", key).unwrap();
            t.reset().unwrap();
            std::process::exit(1);
        }
    }
}


fn add_teleport_to_profile(teleport_name: &str, directory_name: &str) {
    let term_msg = "Need access to the terminal, but couldn't get that";
    let mut t = term::stdout().expect(term_msg);
    let path = std::path::Path::new(directory_name);

    if !path.is_dir() {
        t.fg(term::color::RED).unwrap();
        writeln!(t, "Could not find {}.", directory_name).unwrap();
        writeln!(t, "Is it really a directory").unwrap();
        t.reset().unwrap();
        std::process::exit(1);
    }

    let canonical_path = paths::canonicalize_path(&path.to_path_buf()).display().to_string();
    storage::save_to_current_profile(teleport_name, &canonical_path);

    t.fg(term::color::GREEN).unwrap();
    writeln!(t, "Added '{}' which points to '{}'", teleport_name, canonical_path).unwrap();
    t.reset().unwrap();
}

fn do_remove_from_profile(key: &str) {
    let term_msg = "Need access to the terminal, but couldn't get that";
    let mut t = term::stdout().expect(term_msg);

    if storage::remove_from_profile(key) {
        t.fg(term::color::GREEN).unwrap();
        writeln!(t, "'{}' is no longer a valid teleport", key).unwrap();
    } else {
        t.fg(term::color::RED).unwrap();
        writeln!(t, "'{}' is not a teleport, could not remove", key).unwrap();
        t.reset().unwrap();
        std::process::exit(1);
    }

    t.reset().unwrap();
}

fn add_to_profile(key: &str) {
    let term_msg = "Need access to the terminal, but couldn't get that";
    let mut t = term::stdout().expect(term_msg);

    let items = key.split(":").collect::<Vec<_>>();
    if items.len() == 1 {
        let telepath = std::path::Path::new(items[0]).to_path_buf();
        let canonical = paths::canonicalize_path(&telepath);
        let fname = canonical.file_name().unwrap();
        let as_str = fname.to_str().unwrap();
        add_teleport_to_profile(as_str, items[0]);
    } else if items.len() == 2 {
        add_teleport_to_profile(items[0], items[1]);
    } else {
        t.fg(term::color::RED).unwrap();
        writeln!(
            t,
            "'{}' is not formatted like expected. Format is 'teleport:directory'",
            key
        )
        .unwrap();
        t.reset().unwrap();
        std::process::exit(1);
    }
}

fn do_prefix(key: &str) {
    let profile = storage::get_current_profile().unwrap();

    let matches: Vec<String> = profile
        .keys()
        .filter(|x| x.starts_with(key))
        .map(|x| String::from(x))
        .collect();
    if matches.len() == 0 {
        return;
    } else if matches.len() == 1 {
        println!("{}/", matches[0]);
    } else {
        print!("{}/", matches[0]);
        for k in 1..matches.len() {
            print!(" {}/", matches[k]);
        }
        println!("");
    }
}

fn print_source_install() {
    let path = paths::get_config_script_path("goto").display().to_string();
    println!("");
    println!("# add `goto` command to shell");
    println!("if [ -f {} ]; then", path);
    println!("  source {}", path);
    println!("fi");
    println!("");
}

fn print_powershell_source_install() {
    let path = paths::get_config_script_path("goto-powershell.ps1").display().to_string();
    println!("");
    println!("# goto profile");
    println!("$GotoPath = \"{}\"", path);
    println!("if (Test-Path($GotoPath)) {{");
    println!("  . \"$GotoPath\"");
    println!("}}");
    println!("");
}

fn do_install() {
    storage::install_latest_scripts();
    print_source_install()
}

fn do_powershell_install() {
    storage::install_latest_scripts();
    print_powershell_source_install();
}

fn do_config_dir() {
    let path = paths::get_config_dir().display().to_string();
    println!("{}", path);
}

fn main() {
    ensure_directory_structure();
    let app = parse_opts();
    let matches = app.get_matches();

    if let Some(x) = matches.value_of("add") {
        add_to_profile(x);
    } else if let Some(x) = matches.value_of("get") {
        get_from_profile(x);
    } else if let Some(x) = matches.value_of("remove") {
        do_remove_from_profile(x);
    } else if matches.occurrences_of("list") == 1 {
        list_profile();
    } else if let Some(x) = matches.value_of("prefix") {
        do_prefix(x);
    } else if matches.occurrences_of("install") == 1 {
        do_install();
    } else if matches.occurrences_of("install-powershell") == 1 {
        do_powershell_install();
    } else if matches.occurrences_of("config-dir") == 1 {
        do_config_dir();
    } else {
        parse_opts().write_help(&mut std::io::stdout()).unwrap();
    }
}
