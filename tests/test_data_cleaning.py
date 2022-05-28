import pandas as pd


jobMockData = {
    'company_name': 'LG Energy Solution Michigan, Inc.',
    'location': 'Westborough, MA',
    'job_title': 'Data Scientist',
    'est_salary': '$66K - $120K (Glassdoor est.)',
    'job_description': 'LG Energy Solution (LGES) Vertech is a technology leader in Li-ion based battery energy storage systems (BESS). We provide customizable clean energy storage solutions for renewables integration, commercial & industrial application, and utility-scale installations. LGES-Vertech plays a key role in EV mobility revolution that’s underway. LGES -Vertech is a vertically integrated company providing batteries, power-conversion system, system integration, and operations. LGES-Vertech has installed and maintained services for 1.2+GWHr of BESS in 180+ projects worldwide. Our proprietary AEROS® Energy Management Suite houses diverse data-related services such as data warehousing, remote monitoring, data visualization, and predictive maintenance.\nThe Role\nLGES-Vertech is looking for motivated Data Scientist to join their Data Science and Data Analysis group and be part of renewable energy revolution and be pioneer in creating data science products for the energy systems. The individual in this position would be responsible for solving some of the most complex and challenging issues in BESS products. The data scientist will have the opportunity to innovate new algorithms, expand our suite of data-driven products, and apply data science techniques to provide BESS which is safe, highly available, and efficiently interoperate in the energy market.',
    'rating': '3.2',
    'sector': 'Manufacturing',
    'industry': 'Chemical Manufacturing'
}


def get_mock_data():
    df = pd.DataFrame(data=jobMockData)
    return df


mock_df = get_mock_data()


def test_clean_company_name():
    df = mock_df.copy()
    # df.company_name = df.company_name.str.split('\n')[0]
    df = clean_company_name(df)
    assert 'LG Energy Solution Michigan, Inc.' == df.company_name[0]


def test_clean_est_salary():
    df = mock_df.copy()
    # df.est_salary = df.est_salary.str.split('(')[0]
    # df.est_salary = df.est_salary.str.replace('$', '')
    # df.est_salary = df.est_salary.str.replace('K', '000')
    # df.est_salary = df.est_salary.str.replace(' ', '')
    # df.est_salary = df.est_salary.str.replace('Per Hour', '')
    # df.est_salary = df.est_salary.str.replace('Employer Provided Salary: ', '')
    df = clean_est_salary(df)
    assert '66-120' == df.est_salary[0]
