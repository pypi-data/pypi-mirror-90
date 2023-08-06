//! I/O functionality.

use std::fs::File;

pub fn read_edge_list_csv(
    path: &str,
    delimiter: u8,
) -> Result<csv::DeserializeRecordsIntoIter<File, (usize, usize)>, String> {
    let file = match File::open(path) {
        Err(error) => return Err(error.to_string()),
        Ok(f) => f,
    };
    Ok(csv::ReaderBuilder::new()
        .has_headers(false)
        .delimiter(delimiter)
        .from_reader(file)
        .into_deserialize::<(usize, usize)>())
}
