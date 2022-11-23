import React, { useState } from 'react'
import { DataGrid } from '@mui/x-data-grid';
import { Button, Container, Grid, IconButton, Tooltip, Typography } from '@mui/material';
import { useQuery } from 'react-query';
import axios from '../../../../axios'
import Alert from '@material-ui/lab/Alert';
import EditIcon from '@material-ui/icons/Edit';
import AddIcon from '@material-ui/icons/Add';
import { useNavigate } from 'react-router-dom';
const DatasetList = props => {

    const [error, setError] = useState(null)
    const navigate = useNavigate();
    const getDatasets = async () => {

        try {


            const res = await axios.get("/dataset");

            if (res.error)
                setError(res.error.response.statusText);
            else {
                console.log("getDatasets", res.data)

                return res.data;
            }
        } catch (e) {
            setError(e)

        } finally {

        }
    };
    const { data, isLoading } = useQuery("getDatasets", getDatasets, { refetchInterval: 10000 });

    const columns = [
        { field: 'id', headerName: 'ID', width: 90 },
        {
            field: 'name',
            headerName: 'Name',
            width: 250,

        },
        {
            field: 'created_date',
            headerName: 'Created at',

            width: 200,
            valueGetter: (params) => {

                return params.value && new Date(params.value).toLocaleString();
            }
        },
        {
            field: 'last_modified',
            headerName: 'Last modified at',

            width: 200,
            valueGetter: (params) => {
                return params.value && new Date(params.value).toLocaleString();
            }
            ,
        },
        {
            field: 'status',
            headerName: 'Status',
            width: 100,
            renderCell: (params) => {
                return <p>{`${params.value}`}</p>;
            }
        },
        {
            field: 'source_imagery',
            headerName: 'Imagery',
            width: 100,
            renderCell: (params) => {
                return <Tooltip title={<a target='_blank' rel='noreferrer' href={`${params.value}`}>{`${params.value}`}</a>} aria-label="add">
                    <span> {params.value && "OAM"}</span>
                </Tooltip>;
            }
        },
        {
            field: 'actions',
            headerName: 'Actions',
            width: 200,
            renderCell: (params) => {
                return <IconButton aria-label="comments"
                    onClick={(e) => {
                        navigate(`/training-datasets/${params.row.id}`)
                    }}>
                    <EditIcon />
                </IconButton>
                //  <p>{`${params.row.status} and id ${params.row.id}`}</p>;
            }
        }

    ];

    return <>

        <Grid container padding={2} spacing={2}>
            <Grid item xs={9}>
                <Typography variant="h6" component="div">
                    Training Datasets
                </Typography>
            </Grid>
            <Grid item xs={3}>
                <Grid container justifyContent="flex-end">

                    <Button
                        variant="contained"
                        color="primary"
                        startIcon={<AddIcon />}
                        onClick={()=> {navigate("/training-datasets/new")}}
                    >
                        Create New
                    </Button>
                </Grid>

            </Grid>
            <Grid item xs={12}>
                <Typography variant="body1" component="div">
                    Description long
                </Typography>
            </Grid>
            {error &&
                <Grid item xs={12}>
                    <Alert severity="error">{error}</Alert>

                </Grid>}
            <Grid item xs={12}>
                {isLoading && <p>Loading ... </p>}
                {!isLoading && <div style={{ height: 600, width: '100%' }}>
                    <DataGrid
                        rows={data}
                        columns={columns}
                        pageSize={10}
                        rowsPerPageOptions={[10]}
                        checkboxSelection
                        disableSelectionOnClick

                    />
                </div>}

            </Grid>

        </Grid>
    </>;
}

export default DatasetList;