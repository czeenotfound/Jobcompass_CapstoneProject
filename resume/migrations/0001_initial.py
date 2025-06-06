# Generated by Django 5.1 on 2025-05-09 15:22

import cloudinary.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
        ('industry', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education_level', models.CharField(blank=True, choices=[('high_school', 'High School'), ('associate', 'Associate Degree'), ('bachelor', 'Bachelor’s Degree'), ('master', 'Master’s Degree'), ('doctorate', 'Doctorate (Ph.D.)'), ('vocational', 'Vocational/Technical'), ('other', 'Other')], max_length=20, null=True)),
                ('degree', models.CharField(blank=True, max_length=100)),
                ('institution', models.CharField(blank=True, max_length=100)),
                ('graduation_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('company', models.CharField(blank=True, max_length=100)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(blank=True, max_length=50)),
                ('url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/di2hrzuyq/image/upload/v1733062519/pbnrwanwq7rp17jfr92z.png', max_length=255, verbose_name='avatar')),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('suffix', models.CharField(blank=True, max_length=10)),
                ('about_me', models.TextField(blank=True)),
                ('salary_display_type', models.CharField(blank=True, choices=[('fixed', 'Fixed Salary'), ('range', 'Salary Range'), ('hidden', 'Do not display')], default='hidden', max_length=10, null=True)),
                ('currency', models.CharField(blank=True, choices=[('USD', '$'), ('CAD', 'CA$'), ('EUR', '€'), ('AED', 'AED'), ('AFN', 'Af'), ('ALL', 'ALL'), ('AMD', 'AMD'), ('ARS', 'AR$'), ('AUD', 'AU$'), ('AZN', 'man.'), ('BAM', 'KM'), ('BDT', 'Tk'), ('BGN', 'BGN'), ('BHD', 'BD'), ('BIF', 'FBu'), ('BND', 'BN$'), ('BOB', 'Bs'), ('BRL', 'R$'), ('BWP', 'BWP'), ('BYN', 'Br'), ('BZD', 'BZ$'), ('CDF', 'CDF'), ('CHF', 'CHF'), ('CLP', 'CL$'), ('CNY', 'CN¥'), ('COP', 'CO$'), ('CRC', '₡'), ('CVE', 'CV$'), ('CZK', 'Kč'), ('DJF', 'Fdj'), ('DKK', 'Dkr'), ('DOP', 'RD$'), ('DZD', 'DA'), ('EEK', 'Ekr'), ('EGP', 'EGP'), ('ERN', 'Nfk'), ('ETB', 'Br'), ('GBP', '£'), ('GEL', 'GEL'), ('GHS', 'GH₵'), ('GNF', 'FG'), ('GTQ', 'GTQ'), ('HKD', 'HK$'), ('HNL', 'HNL'), ('HRK', 'kn'), ('HUF', 'Ft'), ('IDR', 'Rp'), ('ILS', '₪'), ('INR', 'Rs'), ('IQD', 'IQD'), ('IRR', 'IRR'), ('ISK', 'Ikr'), ('JMD', 'J$'), ('JOD', 'JD'), ('JPY', '¥'), ('KES', 'Ksh'), ('KHR', 'KHR'), ('KMF', 'CF'), ('KRW', '₩'), ('KWD', 'KD'), ('KZT', 'KZT'), ('LBP', 'L.L.'), ('LKR', 'SLRs'), ('LTL', 'Lt'), ('LVL', 'Ls'), ('LYD', 'LD'), ('MAD', 'MAD'), ('MDL', 'MDL'), ('MGA', 'MGA'), ('MKD', 'MKD'), ('MMK', 'MMK'), ('MOP', 'MOP$'), ('MUR', 'MURs'), ('MXN', 'MX$'), ('MYR', 'RM'), ('MZN', 'MTn'), ('NAD', 'N$'), ('NGN', '₦'), ('NIO', 'C$'), ('NOK', 'Nkr'), ('NPR', 'NPRs'), ('NZD', 'NZ$'), ('OMR', 'OMR'), ('PAB', 'B/.'), ('PEN', 'S/.'), ('PHP', '₱'), ('PKR', 'PKRs'), ('PLN', 'zł'), ('PYG', '₲'), ('QAR', 'QR'), ('RON', 'RON'), ('RSD', 'din.'), ('RUB', 'RUB'), ('RWF', 'RWF'), ('SAR', 'SR'), ('SDG', 'SDG'), ('SEK', 'Skr'), ('SGD', 'S$'), ('SOS', 'Ssh'), ('SYP', 'SY£'), ('THB', '฿'), ('TND', 'DT'), ('TOP', 'T$'), ('TRY', 'TL'), ('TTD', 'TT$'), ('TWD', 'NT$'), ('TZS', 'TSh'), ('UAH', '₴'), ('UGX', 'USh'), ('UYU', '$U'), ('UZS', 'UZS'), ('VEF', 'Bs.F.'), ('VND', '₫'), ('XAF', 'FCFA'), ('XOF', 'CFA'), ('YER', 'YR'), ('ZAR', 'R'), ('ZMK', 'ZK'), ('ZWL', 'ZWL$')], default='PHP', max_length=3, null=True)),
                ('expt_salary_fixed', models.PositiveIntegerField(blank=True, help_text='Enter fixed salary if selected.', null=True)),
                ('expt_salary_min', models.PositiveIntegerField(blank=True, help_text='Enter minimum salary for range.', null=True)),
                ('expt_salary_max', models.PositiveIntegerField(blank=True, help_text='Enter maximum salary for range.', null=True)),
                ('expt_salary_mode', models.CharField(blank=True, choices=[('Hourly', 'Hourly'), ('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly'), ('Yearly', 'Yearly')], max_length=20, null=True)),
                ('job_position', models.CharField(blank=True, max_length=150)),
                ('location_job_type', models.CharField(blank=True, choices=[('Remote', 'Remote'), ('Onsite', 'Onsite'), ('Hybrid', 'Hybrid')], max_length=20)),
                ('employment_job_type', models.CharField(blank=True, choices=[('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time'), ('Contract', 'Contract'), ('Freelance', 'Freelance'), ('Internship/OJT', 'Internship/OJT')], max_length=20)),
                ('upload_resume', cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='file')),
                ('address', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resumes', to='address.address')),
                ('industry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='industry.industry')),
            ],
        ),
    ]
