#include <iostream>
#include <string>
#include <string.h>
#include<conio.h>

using namespace std;
/// <summary>
/// Prison class have all the attributes of prisoner and it is base class so, we made it abstract. Abstration 
/// Prisoner Details class is child class of Prison and have an overloadind of functions to print deatails. Polymorphism
/// Release Prison classs have implementation to to del the data of given prisoner from the object of array.
/// Attendances class have the implementation to take attendance of prisoners.
/// Guard Class is genrating guards automatically to the number of cells and give unique ids to gurads and assign duty of each guard to the each cell.
/// Generic Global Function applying Linear Search Algorithm for Searching Prisoners.
/// Global Show() function is to design the interface.
/// Global Login() function is to apply login system.  
/// </summary>
class Prison
{
public:
    string name;
    string crime;
    int cellno;
    int age;
    int duration;
    string dateofentry;
    string ID;
public:
    Prison()
    {

    }
    Prison(string n,string cr, int ce, int a, int d, string doe)
    {
        name = n;
        crime = cr;
        cellno = ce;
        age = a;
        duration = d;
        dateofentry = doe;
    }
    void setname(string n)
    {
        name = n;
    }
    void setcrime(string c)
    {
        crime = c;
    }
    void setid(string id)
    {
        ID = id;
    }
    void setcellno(int cl)
    {
        cellno = cl;
    }
    void setage(int a)
    {
        age = a;
    }
    void setduration(int d)
    {
        duration = d;
    }
    void setdateofentry(string doe)
    {
        dateofentry = doe;
    }
     virtual int getcellno() = 0;
     virtual string getID() = 0;
};
class PrisonersDetails : public Prison
{
public:
    PrisonersDetails(string n, string cr, int ce, int a, int d, string doe) : Prison(n, cr, ce, a, d, doe)
    {

    }
    PrisonersDetails()
    {}
    
    void print()
    {
        cout << "\t\t__Prisoner Data__" << endl;
        cout << "\n\n";
        cout << "Name\t Crime\t\t\t ID\t\t\t Cellno\t Age\t Duration\t Date of Entry\n";
        cout << "-----------------------------------------------------------------------";
        cout << endl;
    }
    void print(int )
    {
        cout << name << "\t" << crime << "\t\t\t"<<ID<<"\t\t" << cellno << "\t" << age << "\t" << duration << "\t" << dateofentry;
        cout << endl;
    }
    int getcellno()
    {
        return cellno;
    }
    string getID()
    {
        return ID;
    }
};
template<typename T>bool search(T pf[], int n) 
{
    bool found = false;
    string idsearch;
    cout << "Enter the ID for Searching Prisoners: ";
    cin >> idsearch;
    for (int i = 0; i < n; i++)
    {
        if (pf[i].getID() == idsearch)
        {
            found = true;
            pf[i].print();
            pf[i].print(1);
            break;
        }
    }
  //  cout << "\t\t\tPrisoner Not Found!"<<endl;
    return false;
}
class ReleasePrisoners : private PrisonersDetails
{
    string priID;
public:
    ReleasePrisoners(){}
    void releasePrisoner(int n, PrisonersDetails p[])
    {
        
        cout << "Enter the ID of Prisoner: ";
        cin >> priID;
        for (int i = 0; i < n; i++)
        {
            if (priID == p[i].getID())
            {
                for (int j = i; j < n - 1; j++)
                {
                    p[j] = p[j + 1];
                }
                n--;
                cout << "\t\t\tPrisoner released successfully!" << endl;
                cout << "\t\t\tNow,";
                break;
            }
        }
        if (priID != p[n - 1].ID)
        {
            cout << "Prisoner with ID :" << priID << " not found!" << endl;
        }
    }
};
class guards
{
    string guardid;
    int dutycell;
public:
    guards()
    {}
    guards(string id, int dc)
    {
        guardid = id;
        dutycell = dc;
    }
    void setdutycell(int dc)
    {
        dutycell = dc;
    }
    void display(int)
    {
        cout << "Guard ID" << "\t\t\t" << "DutyCell" << endl;
        cout << "---------------------------------------------------------------" << endl;
    }
    void display()
    {
        cout <<"\t\t\t"<<srand << "\t\t\t\t" << dutycell << endl;
    }
};
class Attendance 
{
    string date;
public:
    void setdate(string d)
    {
        date = d;
    }
    void TakingAttendance(int n,PrisonersDetails p[])
    {
        char* c;
        c = new char[n];
        cout << "Prisoner of ID: \t\t\t" << date<<"\t\t" << endl;
        cout << "-------------------------------------------------------" << endl;
        for (int i = 0; i < n; i++)
        {
            
            cout << p[i].getID() << "\t\t\t\t";
            cin >> c[i];
        }
        system("cls");
        cout << endl << endl;
        cout << "\t\t\t\tAttendance Locked\n\n";
        cout << "Prisoner of ID: \t\t\t" << date << "\t\t" << endl;
        cout << "-------------------------------------------------------" << endl;
        for (int i = 0; i < n; i++)
        {

            cout << p[i].getID()<<"\t\t\t\t"<<c[i]<<endl;
           
        }
    }
};
int n;
void show()
{
    string nn = { "Enter Your Choice:\n 1) Print Details \n 2) Release Prisoners \n 3) Guards Dutycells \n 4) Attendance of Prisoners \n 5) Searching \n 6) Logout: " };

    cout << "\t\t";
    int s = nn.size();
    for (int i = 0; i < s; i++)
    {
        cout << nn[i];
        for (int j = 0; j < 10000000; j++)
        {
        }
    }
    
}
void Login()
{
    string username = { "iqrafahad" };
    string password = { "ooplab" };
    string usernameinput;
    string passwordinput;
    char ch;
    cout << "\n\n\n";
    cout << "\t\t\t-------------------------------" << endl;
    cout << "\t\t\t\tUsername: ";
    cin >> usernameinput;
    cout << endl;
    cout << "\t\t\t\tPassword: ";

    while ((ch = _getch()) != 13) //enter type
    {
        passwordinput += ch;
        cout << '*';
    }
    cout << "\t\t\t-------------------------------" << endl;
    int r = username.compare(usernameinput);
    int s = password.compare(passwordinput);
    if (r == 0 && s == 0)
    {
        system("cls");
        string nn = { "_Welcome To The Prison Management System_" };
        cout << "\t\t";
        int s = nn.size();
        for (int i = 0; i < s; i++)
        {
            cout << nn[i];

            for (int j = 0; j < 10000000; j++)
            {
            }
        }
        cout << endl;
    }
    else
    {
        system("cls");
        cout << "\t\t\tAccess Denied!";
        exit(1);
    }
}
int main()
{
    int c;
    Login();
    PrisonersDetails* p;
    static int m;
    string na[100];
    string cr[100];
    int cell[100];
    int a[100];
    int d[100];
    string date[100];
    string id[100];
    int s;
    int r;
    int x;
    while (1)
    {
     cout << "Enter number of prisoners: ";
     cin >> n;
     p = new PrisonersDetails[n];
            if (n != 0)
            {

                for (int i = 0; i < n; i++)
                {
                    cout << "Enter the name of Prisoner " << i + 1 << ": ";
                    cin >> na[i];
                }
                cout << endl;
                for (int i = 0; i < n; i++)
                {
                    cout << "Enter the Crime of Prisoner " << i + 1 << ": ";
                    cin >> cr[i];
                }
                cout << endl;
                for (int i = 0; i < n; i++)
                {
                    cout << "Enter the ID of Prisoner " << i + 1 << ": ";
                    cin >> id[i];
                }
                cout << endl;
                for (int i = 0; i < n; i++)
                {
                    cout << "Enter the Cell number of Prisoner " << i + 1 << ": ";
                    cin >> cell[i];
                }
                cout << endl;
                for (int i = 0; i < n; i++)
                {
                    cout << "Enter the age of Prisoner " << i + 1 << ": ";
                    cin >> a[i];
                }
                cout << endl;
                for (int i = 0; i < n; i++)
                {
                    cout << "Enter the Duration of Prisoner " << i + 1 << ": ";
                    cin >> d[i];
                }
                cout << endl;
                for (int i = 0; i < n; i++)
                {
                    cout << "Enter the Date of Entry of Prisoner " << i + 1 << ": ";
                    cin >> date[i];
                }
                for (int i = 0; i < n; i++)
                {
                    p[i].setname(na[i]);
                    p[i].setcrime(cr[i]);
                    p[i].setid(id[i]);
                    p[i].setcellno(cell[i]);
                    p[i].setage(a[i]);
                    p[i].setduration(d[i]);
                    p[i].setdateofentry(date[i]);
                }
                system("cls");
                cout << "\n";
                cout << "\t\tData Successfully entered into the system!"<<endl;
                cout << "\n";
            }
            for (;;)
            {
                show();
                cin >> x;
                switch (x)
                {
                case 1:
                {
                    PrisonersDetails P1;
                    system("cls");
                    P1.print();
                    for (int i = 0; i < n; i++)
                    {
                        p[i].print(2);
                    }

                    break;
                }
                case 2:
                {
                    ReleasePrisoners pr;
                    pr.releasePrisoner(n, p);

                    break;
                }
                case 3:
                {
                    guards* g;
                    g = new guards[n];
                    guards g1;
                    for (int i = 0; i < n; i++)
                    {
                        g[i].setdutycell(p[i].getcellno());
                    }
                    system("cls");
                    cout << endl << endl;
                    cout << "\t\t\t";
                    g1.display(2);
                    for (int i = 0; i < n; i++)
                    {
                        g[i].display();
                    }
                    break;
                }
                case 4:
                {
                    Attendance a1;
                    string d;
                    cout << "Enter the date for Attendance: ";
                    cin >> d;
                    a1.setdate(d);
                    a1.TakingAttendance(n, p);
                    break;
                }
                case 5:
                {
                    system("cls");
                    search(p, n);
                    break;
                }
                case 6:
                {
                    string nn = { " loading-------" };
                    int s = nn.size();
                    system("cls");
                    cout << "\n\n\n";
                    cout << "\t\t\t\t";
                    for (int i = 0; i < s; i++)
                    {
                        cout << nn[i];
                        for (int j = 0; j < 100000000; j++)
                        {
                        }
                    }
                    system("cls");
                    cout << endl << "\n\n\t\t\t\tLOGGEDOUT" << endl;
                    exit(1);
                }
                default:
                    break;
                }


                cout << "Press 1 to continue ";
                cin >> c;
                if (c != 1)
                {
                    break;
                }
            }
    }
}
